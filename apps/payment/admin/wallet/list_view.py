from django.utils.translation import gettext_lazy as _


class WalletListView:
    list_display = (
        "display_header",
        "display_balance",
        "is_use_wallet_in_payment",
        "display_last_update",
    )
    list_editable = ()
    list_filter = ("is_use_wallet_in_payment",)
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ("user__customer__full_name",)
    search_help_text = _("Search by customer name...")

    def get_ordering(self, request):
        return ()
