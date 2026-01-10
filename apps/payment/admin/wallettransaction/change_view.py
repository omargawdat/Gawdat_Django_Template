from django.utils.translation import gettext_lazy as _


class WalletTransactionChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (_("Basic Information"), {"fields": ("wallet", "transaction_type")}),
        (_("Financial Details"), {"fields": ("amount",)}),
        (_("Additional Information"), {"fields": ("transaction_note", "attachment")}),
    )
