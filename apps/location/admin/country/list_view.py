from django.utils.translation import gettext_lazy as _


class CountryListView:
    list_display = (
        "display_header",
        "code",
        "currency",
        "display_is_active_country",
    )
    list_editable = ()
    list_filter = ["is_active", "code"]
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ["code"]
    search_help_text = _("Search by code...")

    def get_ordering(self, request):
        return ()
