from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import MultipleRelatedDropdownFilter


class RegionListView:
    list_display = ("display_header", "name", "code", "display_is_active_region")
    list_editable = ()
    list_filter = [("country", MultipleRelatedDropdownFilter), "country"]
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ["name"]
    search_help_text = _("Search By Name...")

    def get_ordering(self, request):
        return ()
