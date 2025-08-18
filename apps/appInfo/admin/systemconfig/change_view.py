class SystemConfigChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (("System Config", {"fields": ("cancellation_fees",)}),)
