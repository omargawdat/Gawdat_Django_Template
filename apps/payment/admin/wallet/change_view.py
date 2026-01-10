from django.utils.translation import gettext_lazy as _

from apps.payment.admin.wallettransaction.inline import WalletTransactionInline


class WalletChangeView:
    filter_horizontal = ()
    compressed_fields = False
    autocomplete_fields = ()
    fieldsets = (
        (
            _("Information"),
            {"fields": ("user", "balance", "is_use_wallet_in_payment", "last_update")},
        ),
    )
    inlines = [WalletTransactionInline]
