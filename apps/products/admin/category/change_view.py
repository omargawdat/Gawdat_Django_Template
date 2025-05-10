class CategoryChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (("Cateogry Information", {"fields": ("name", "image")}),)
