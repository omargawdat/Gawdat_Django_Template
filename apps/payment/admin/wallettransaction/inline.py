from apps.payment.models.wallet_transaction import WalletTransaction
from common.base.admin import BaseTabularInline

from .permissions import WalletTransactionInlinePermissions


class WalletTransactionInline(WalletTransactionInlinePermissions, BaseTabularInline):
    model = WalletTransaction
    extra = 0
    show_change_link = True
    fields = ["id", "transaction_type", "amount", "created_at", "action_by"]
    autocomplete_fields = ()
