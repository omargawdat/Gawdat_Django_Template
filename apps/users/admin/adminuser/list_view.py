class AdminUserListView:
    list_display = ("display_header", "display_date_joined_time", "is_active")
    list_editable = ("is_active",)
    list_filter = ()
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = False
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ("username",)
    search_help_text = "Search by username"

    def get_ordering(self, request):
        return ()
