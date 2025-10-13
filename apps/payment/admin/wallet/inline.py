from apps.payment.models.wallet import Wallet
from common.base.admin import BaseTabularInline

from .permissions import WalletInlinePermissions


class WalletInline(WalletInlinePermissions, BaseTabularInline):
    """
    Wallet inline for User admin.
    Note: Cannot be used with Customer admin since Wallet -> User relationship.
    """

    model = Wallet
    extra = 0
    show_change_link = True
    tab = True
    fields = ("balance", "is_use_wallet_in_payment", "last_update")
    readonly_fields = ("balance", "last_update")
    autocomplete_fields = ()
