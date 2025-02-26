from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationTypes(models.TextChoices):
    OTHER = "OTHER", _("Other")


NOTIFICATION_MESSAGES = {
    NotificationTypes.OTHER: {
        "en": {"title": "Notification", "body": "{message}"},
        "ar": {"title": "إشعار", "body": "{message}"},
    },
}
