from django.templatetags.static import static
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.channel.constants import NotificationType
from apps.channel.models.notification import Notification


class NotificationDisplayMixin:
    @display(description=_("Notification ID"), header=True)
    def display_header(self, notification: Notification):
        """Display header with image if available."""
        notification_image = static("images/notification.png")
        return [
            notification.pk,
            "",
            _("O"),
            {
                "path": notification.image.url
                if hasattr(notification, "image") and notification.image
                else notification_image
            },
        ]

    @display(
        description=_("Notification Type"),
        label={
            NotificationType.OTHER.label: "success",
        },
    )
    def display_notification_type(self, notification: Notification):
        return notification.get_notification_type_display()

    @display(description=_("Created ago"), ordering="created_at", label=_("info"))
    def display_created_time(self, notification: Notification):
        return f"{timesince(notification.created_at, timezone.now())}"
