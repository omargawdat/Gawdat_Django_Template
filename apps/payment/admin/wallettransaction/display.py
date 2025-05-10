from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.payment.constants import WalletTransactionType
from apps.payment.models.wallet_transaction import WalletTransaction


class WalletTransactionDisplayMixin:
    @display(description="wallet_transaction", header=True)
    def display_header(self, wallet_transaction: WalletTransaction):
        """Display header with image if available."""
        return [
            f"Transaction ID: {wallet_transaction.pk}",
            f"Customer: {wallet_transaction.wallet.user.username}",
            "",
            "O",
            {
                "path": wallet_transaction.image.url
                if hasattr(wallet_transaction, "image") and wallet_transaction.image
                else None
            },
        ]

    @display(description=_("Created ago"), ordering="created_at", label="info")
    def display_created_time(self, wallet_transaction: WalletTransaction):
        return f"{timesince(wallet_transaction.created_at, timezone.now())}"

    @display(
        description=_("Transaction Type"),
        ordering="transaction_type",
        label={
            WalletTransactionType.REFUND.label: "success",
            WalletTransactionType.FINE.label: "danger",
            WalletTransactionType.PAYOUT.label: "warning",
            WalletTransactionType.CHARGING.label: "info",
            WalletTransactionType.ORDER_PAYMENT.label: "primary",
            WalletTransactionType.CANCEL_ORDER.label: "secondary",
            WalletTransactionType.SHARE.label: "success",
            WalletTransactionType.CASH_RECEIVE.label: "danger",
        },
    )
    def display_transaction_type(self, wallet_transaction: WalletTransaction):
        return wallet_transaction.get_transaction_type_display()

    @display(description=_("Amount"), ordering="amount", label="info")
    def display_amount(self, wallet_transaction: WalletTransaction):
        return (
            f"{wallet_transaction.amount.amount} {wallet_transaction.amount.currency}"
        )
