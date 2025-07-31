class BannerGroupChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        ("Information", {"fields": ("name_ar", "name_en", "order", "is_active")}),
    )
