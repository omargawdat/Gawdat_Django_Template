class BannerChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (("Banner Image", {"fields": ("image", "banner_type")}),)
