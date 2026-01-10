from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import RangeDateFilter

from apps.location.admin.address.inline import AddressInline

from .sections import ClientTableSection


class CustomerListView:
    list_display = (
        "display_customer_info",
        "primary_address",
        "display_total_spend",
        "display_is_active_customer",
        "display_date_joined_time",
    )
    list_editable = ()
    list_filter = (("user__date_joined", RangeDateFilter), "user__is_active", "country")
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = True
    search_fields = ["user__email", "full_name"]
    search_help_text = _("search by email or full name...🔍")
    ordering = ("-user__date_joined",)
    inlines = [AddressInline]
    list_sections = [ClientTableSection]
