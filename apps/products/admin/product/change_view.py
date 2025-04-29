class ProductChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ("category",)
    fieldsets = (
        ("Basic Information", {"fields": ("name", "description")}),
        ("Pricing", {"fields": ("price",)}),
        ("Categorization", {"fields": ("category",)}),
        ("Media", {"fields": ("image",)}),
    )
