from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import ChoicesDropdownFilter


class CountryListView:
    list_display = (
        "display_header",
        "code",
        "currency",
        "display_is_active_country",
    )
    list_editable = ()
    list_filter = ["is_active", ("currency", ChoicesDropdownFilter), "code"]
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ["name"]
    search_help_text = _("Search by name...")

    def get_ordering(self, request):
        return ()
