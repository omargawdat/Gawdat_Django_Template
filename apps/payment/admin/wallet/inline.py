from apps.payment.models.wallet import Wallet
from common.base.admin import BaseTabularInline

from .permissions import WalletInlinePermissions


class WalletInline(WalletInlinePermissions, BaseTabularInline):
    model = Wallet
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
