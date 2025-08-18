from django.utils.translation import gettext_lazy as _


class CountryChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            _("Country Information"),
            {
                "fields": (
                    "code",
                    "name",
                    "currency",
                    "phone_code",
                    "flag",
                    "is_active",
                )
            },
        ),
        (
            _("Referral Points"),
            {"fields": ("referral_points",)},
        ),
    )
