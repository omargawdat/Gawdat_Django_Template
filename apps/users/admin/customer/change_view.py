from django.utils.translation import gettext_lazy as _


class CustomerChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()

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
                    "in",
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
                "classes": ("collapse",),
            },
        ),
    )
