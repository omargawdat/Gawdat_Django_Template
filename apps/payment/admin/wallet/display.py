from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.payment.models.wallet import Wallet


class WalletDisplayMixin:
    @display(description=_("Customer"), header=True)
    def display_header(self, wallet: Wallet):
        """Display header with image if available."""
        return [
            wallet.user.customer.email or wallet.user.customer.email,
            "",
            "O",
            {
                "path": wallet.user.customer.image
                if wallet.user.customer.image
                else None
            },
        ]

    @display(description=_("Balance"), ordering="balance", label="info")
    def display_balance(self, wallet: Wallet):
        return f"{wallet.balance.amount} {wallet.balance.currency}"

    @display(description=_("Last Update ago"), ordering="last_update", label="info")
    def display_last_update(self, wallet: Wallet):
        return f"{timesince(wallet.last_update, timezone.now())}"
