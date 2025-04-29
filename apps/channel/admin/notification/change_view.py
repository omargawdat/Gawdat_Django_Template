from django.utils.translation import gettext_lazy as _


class NotificationChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = []

    fieldsets = (
        (
            _("Notification 📢"),
            {
                "fields": ("title", "message_body"),
            },
        ),
        (
            _("Users 👥"),
            {
                "fields": ("users",),
            },
        ),
        (
            _("Choices"),
            {
                "fields": ("notification_type",),
            },
        ),
    )
