from django.utils.translation import gettext_lazy as _


class AddressChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            _("Customer Address"),
            {
                "fields": (
                    "customer",
                    "point",
                    "description",
                    "location_type",
                    "map_description",
                )
            },
        ),
    )
