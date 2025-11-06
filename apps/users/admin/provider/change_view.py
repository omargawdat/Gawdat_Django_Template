from django.utils.translation import gettext_lazy as _


class ProviderChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()

    # User-related fields are readonly (they're on the User model, not Provider)
    readonly_fields = ("email", "date_joined", "is_active")

    fieldsets = (
        (
            _("Provider Information🏢"),
            {
                "fields": (
                    "company_name",
                    "email",
                )
            },
        ),
        (
            _("Advanced Settings🔧"),
            {
                "fields": (
                    "date_joined",
                    "is_active",
                ),
            },
        ),
    )
