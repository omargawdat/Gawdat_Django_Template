from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import RangeDateFilter

from apps.location.admin.address.inline import AddressInline
from apps.payment.admin.wallet.inline import WalletInline


class CustomerListView:
    list_display = (
        "display_customer_info",
        "primary_address",
        "gender",
        "display_is_active_customer",
        "display_date_joined_time",
    )
    list_editable = ()
    list_filter = (("date_joined", RangeDateFilter), "is_active", "country")
    date_hierarchy = "date_joined"
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = True
    search_fields = ["phone_nnumber"]
    search_help_text = _("search phone...🔍")
    ordering = ("-date_joined",)
    inlines = [AddressInline, WalletInline]
