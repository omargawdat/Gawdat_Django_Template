from django.utils.translation import gettext_lazy as _


class CustomerChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()

    # User-related fields are readonly (they're on the User model, not Customer)
    readonly_fields = ("username", "phone_number", "email", "date_joined", "is_active")

    fieldsets = (
        (
            _("Customer Information👨‍🦰"),
            {
                "fields": (
                    "full_name",
                    "username",
                    "phone_number",
                    "email",
                    "image",
                    "gender",
                    "birth_date",
                    "primary_address",
                    "country",
                )
            },
        ),
        (
            _("Advanced Settings🔧"),
            {
                "fields": (
                    "inviter",
                    "date_joined",
                    "is_active",
                    "is_verified",
                ),
            },
        ),
    )
