from django.utils.translation import gettext_lazy as _


class AdminUserChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            _("Admin Info"),
            {
                "fields": (
                    "image",
                    "email",
                    "password",
                    "groups",
                    "user_permissions",
                    "is_active",
                    "can_access_money",
                )
            },
        ),
    )
