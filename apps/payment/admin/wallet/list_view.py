from unfold.contrib.filters.admin import RangeNumericFilter

from apps.payment.admin.wallettransaction.inline import WalletTransactionInline


class WalletListView:
    list_display = (
        "display_header",
        "display_balance",
        "display_last_update",
        "display_is_use_wallet_in_payment",
    )
    list_editable = ()
    list_filter = ["is_use_wallet_in_payment", ("balance", RangeNumericFilter)]
    date_hierarchy = "last_update"
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = True
    search_fields = ("user__customer__phone_number",)
    search_help_text = "search by phone number"

    inlines = [WalletTransactionInline]

    def get_ordering(self, request):
        return ("-last_update",)
