from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.notification.other.constants import NotificationTypes
from apps.users.models import User


class Notification(models.Model):
    users = models.ManyToManyField(User, verbose_name=_("Users"))
    notification_type = models.CharField(
        _("Notification Type"),
        choices=NotificationTypes.choices,
        default=NotificationTypes.OTHER,
    )
    title = models.CharField(_("Title"), max_length=255)
    message_body = models.TextField(_("Message Body"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.title}"
