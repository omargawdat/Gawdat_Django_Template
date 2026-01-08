from django.utils.translation import gettext_lazy as _


class ContactUsChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            _("Information"),
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
