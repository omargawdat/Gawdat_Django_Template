class CategoryListView:
    list_display = ("display_header", "name", "display_products_count")
    list_editable = ()
    list_filter = ()
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = False
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ("name",)
    search_help_text = "search by name"

    def get_ordering(self, request):
        return ()
