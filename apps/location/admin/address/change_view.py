class AddressChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            "Customer Address",
            {
                "fields": (
                    "customer",
                    "point",
                    "description",
                    "location_type",
                )
            },
        ),
    )
