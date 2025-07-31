class OnboardingListView:
    list_display = ("display_header", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ()
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = False
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ()
    search_help_text = ""
    ordering = ("order",)
