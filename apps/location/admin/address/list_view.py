class AddressListView:
    list_display = ("display_header", "customer")
    list_editable = ()
    list_filter = ()
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = False
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ()
    search_help_text = ""

    def get_ordering(self, request):
        return ()
