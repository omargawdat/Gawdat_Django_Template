from django.utils.translation import gettext_lazy as _


class ProductListView:
    list_display = ("display_header", "category", "price")
    list_editable = ()
    list_filter = ("category",)
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = False
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ("name",)
    search_help_text = _("Search by name")

    def get_ordering(self, request):
        return ()
