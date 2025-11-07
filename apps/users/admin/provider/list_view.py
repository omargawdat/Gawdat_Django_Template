from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import RangeDateFilter


class ProviderListView:
    list_display = (
        "display_provider_info",
        "company_name",
        "display_is_active_provider",
        "display_date_joined_time",
    )
    list_editable = ()
    list_filter = (("user__date_joined", RangeDateFilter), "user__is_active")
    date_hierarchy = "user__date_joined"
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = True
    search_fields = ["user__email", "company_name"]
    search_help_text = _("search email or company name...🔍")
    ordering = ("-user__date_joined",)
