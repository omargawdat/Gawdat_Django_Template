from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.payment.api.wallet.serializers import WalletDetailedSerializer
from apps.payment.api.wallet.serializers import WalletUpdateSerializer
from apps.payment.api.wallet_transaction.pagination import (
    WalletTransactionCursorPagination,
)
from apps.payment.api.wallet_transaction.serializers import (
    WalletTransactionDetailedSerializer,
)
from apps.payment.domain.selectors.wallet_transactions import WalletTransactionSelector


class RechargeWalletAPIView(APIView):
    authentication_classes = []
    permission_classess = []
    serializer_class = None


class WalletDetailAPI(APIView):
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
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
