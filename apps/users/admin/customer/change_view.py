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
                    "phone_number",
                    "email",
                    "image",
                    "gender",
                    "birth_date",
                    "primary_address",
                )
            },
        ),
        (
            _("Advanced Settings🔧"),
            {
                "fields": (
                    "is_active",
                    "date_joined",
                    "country",
                    "username",
                ),
                "classes": ("collapse",),
            },
        ),
    )
