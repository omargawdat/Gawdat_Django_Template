class BrandChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (("Brand Logo", {"fields": ("name", "logo")}),)
