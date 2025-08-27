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
                )
            },
        ),
        (
            _("Advanced Settings🔧"),
            {
                "fields": (
                    "referral_customer_id",
                    "date_joined",
                    "is_active",
                ),
                "classes": ("collapse",),
            },
        ),
    )
