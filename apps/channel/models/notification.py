from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.channel.constants import NotificationType
from apps.users.models import User


class Notification(models.Model):
    users = models.ManyToManyField(User, verbose_name=_("Users"))
    title = models.CharField(_("Title"), max_length=255)
    message_body = models.TextField(_("Message Body"))
    notification_type = models.CharField(
        _("Notification Type"),
        choices=NotificationType.choices,
        default=NotificationType.OTHER,
    )
    send_sms = models.BooleanField(_("Send SMS"))
    send_fcm = models.BooleanField(_("Send FCM"))
    object_id = models.PositiveIntegerField(_("Object ID"), null=True, blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.title}"
