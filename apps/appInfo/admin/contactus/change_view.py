class ContactUsChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "customer",
                    "contact_type",
                    "description",
                    "has_checked",
                    "created_at",
                )
            },
        ),
    )
