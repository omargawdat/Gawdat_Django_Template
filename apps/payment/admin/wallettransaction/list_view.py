from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.contrib.filters.admin import RangeNumericFilter


class WalletTransactionListView:
    list_display = (
        "display_header",
        "display_transaction_type",
        "display_amount",
        "display_created_time",
    )
    list_editable = ()
    list_filter = [
        ("created_at", RangeDateFilter),
        ("amount", RangeNumericFilter),
        "action_by",
        "transaction_type",
    ]
    date_hierarchy = "created_at"
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = True
    search_fields = ("wallet__user__username",)
    search_help_text = _("Search by customer phone number")

    def get_ordering(self, request):
        return ()
