from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.contrib.filters.admin import RangeNumericFilter


class PaymentListView:
    list_display = (
        "display_header",
        "display_payment_type",
        "display_payment_price",
        "is_paid",
        "display_created_at_time",
    )

    list_editable = ()
    list_filter = (
        "is_paid",
        ("price_after_discount", RangeNumericFilter),
        ("created_at", RangeDateFilter),
    )
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ("customer__full_name",)
    search_help_text = _("Search by customer name...")
    ordering = ["-created_at"]
