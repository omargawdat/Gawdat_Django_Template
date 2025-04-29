from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.payment.models.wallet import Wallet


class WalletDisplayMixin:
    @display(description=_("Wallet"), header=True)
    def display_header(self, wallet: Wallet):
        return [
            wallet.user,
            wallet.user.full_name,
            "WA",
            {"path": wallet.user.image.url if wallet.user.image else None},
        ]

    @display(description=_("Balance"), ordering="balance", label="info")
    def display_balance(self, wallet: Wallet):
        return f"{wallet.balance.amount} {wallet.balance.currency}"

    @display(
        label={"True": "success", "False": "danger"},
        description=_("Is Use Wallet In Payment?"),
    )
    def display_is_use_wallet_in_payment(self, wallet: Wallet) -> str:
        return "True" if wallet.is_use_wallet_in_payment else "False"

    @display(description=_("Last Update ago"), ordering="last_update", label="info")
    def display_last_update(self, wallet: Wallet):
        return f"{timesince(wallet.last_update, timezone.now())}"
