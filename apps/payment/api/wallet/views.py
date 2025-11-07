from django.db import transaction
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.api.wallet.serializers import WalletDetailedSerializer
from apps.payment.api.wallet.serializers import WalletRechargeSerializer
from apps.payment.api.wallet.serializers import WalletUpdateSerializer
from apps.payment.api.wallet_transaction.pagination import (
    WalletTransactionCursorPagination,
)
from apps.payment.api.wallet_transaction.serializers import (
    WalletTransactionDetailedSerializer,
)
from apps.payment.constants import PaymentType
from apps.payment.domain.selectors.wallet_transactions import WalletTransactionSelector
from apps.payment.domain.services.payment import PaymentService
from apps.payment.domain.utilities.money import WalletUtilities
from apps.payment.models.payment import Payment


class WalletRechargeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletRechargeSerializer

    @extend_schema(
        tags=["Account/Wallet"],
        operation_id="rechargeWallet",
        request={
            "application/json": WalletRechargeSerializer,
        },
        responses={
            200: inline_serializer(
                name="WalletRechargeResponse",
                fields={
                    "payment_url": serializers.URLField(),
                },
            ),
        },
    )
    @transaction.atomic
    def post(self, request):
        user = request.user

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]
        currency = user.wallet.balance.currency
        amount_of_money = WalletUtilities.to_money_obj(amount, currency)

        payment = Payment.objects.create(
            customer=user,
            payment_type=PaymentType.charge_wallet,
            price_before_discount=amount_of_money,
            price_after_discount=amount_of_money,
            is_paid=False,
        )

        payment_url = PaymentService.initialize_online_payment(payment)

        return Response(
            {
                "payment_url": payment_url,
            }
        )


class WalletDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Wallet"],
        operation_id="listWalletDetails",
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="WalletTransactionResponse",
                    fields={
                        "wallet": WalletDetailedSerializer(),
                        "wallet_transactions": inline_serializer(
                            name="PaginatedWalletTransactions",
                            fields={
                                "next": serializers.URLField(allow_null=True),
                                "previous": serializers.URLField(allow_null=True),
                                "results": WalletTransactionDetailedSerializer(
                                    many=True
                                ),
                            },
                        ),
                    },
                ),
            ),
        },
    )
    def get(self, request):
        # Paginate wallet transactions
        wallet_queryset = WalletTransactionSelector.user_wallet_transactions(
            request.user
        )
        wallet_paginator = WalletTransactionCursorPagination()
        wallet_page = wallet_paginator.paginate_queryset(wallet_queryset, request)
        wallet_serializer = WalletTransactionDetailedSerializer(
            wallet_page, many=True, context={"request": request}
        )

        wallet_data = None
        if not request.query_params.get(wallet_paginator.cursor_query_param):
            wallet = request.user.wallet
            wallet_data = WalletDetailedSerializer(wallet).data

        response_data = {
            "wallet": wallet_data,
            "wallet_transactions": {
                "next": wallet_paginator.get_next_link(),
                "previous": wallet_paginator.get_previous_link(),
                "results": wallet_serializer.data,
            },
        }

        return Response(response_data, status=status.HTTP_200_OK)


class WalletUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Wallet"],
        operation_id="updateWallet",
        request={
            "application/json": WalletUpdateSerializer,
        },
        responses={
            200: WalletDetailedSerializer,
        },
    )
    def patch(self, request):
        wallet = request.user.wallet

        serializer = WalletUpdateSerializer(wallet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_wallet = serializer.save()

        response_serializer = WalletDetailedSerializer(updated_wallet)
        return Response(response_serializer.data)
