from unfold.contrib.filters.admin import RangeNumericFilter


class PopUpBannerListView:
    list_display = ("display_header", "display_views", "count_per_user", "is_active")
    list_editable = ("count_per_user", "is_active")
    list_filter = (("count_per_user", RangeNumericFilter), "is_active")
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ()
    search_help_text = ""

    def get_ordering(self, request):
        return ()
