class PopUpBannerChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (("Information", {"fields": ("image", "count_per_user", "is_active")}),)
