class AdminUserChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            "Admin Info",
            {
                "fields": (
                    "image",
                    "username",
                    "password",
                    "groups",
                    "user_permissions",
                    "is_active",
                    "can_access_money",
                )
            },
        ),
    )
