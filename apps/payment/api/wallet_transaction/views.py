from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.api.wallet_transaction.pagination import (
    WalletTransactionCursorPagination,
)
from apps.payment.api.wallet_transaction.serializers import WalletDetailedSerializer
from apps.payment.api.wallet_transaction.serializers import (
    WalletTransactionDetailedSerializer,
)
from apps.payment.domain.selectors.wallet_transactions import WalletTransactionSelector
from apps.payment.models.wallet import Wallet


class TransactionsView(APIView):
    permission_classes = [IsAuthenticated]

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

        try:
            wallet = request.user.wallet
            wallet_data = WalletDetailedSerializer(wallet).data
        except Wallet.DoesNotExist:
            wallet_data = None

        # Construct response
        response_data = {
            "wallet": wallet_data,
            "wallet_transactions": {
                "next": wallet_paginator.get_next_link(),
                "previous": wallet_paginator.get_previous_link(),
                "results": wallet_serializer.data,
            },
        }

        return Response(response_data, status=status.HTTP_200_OK)
