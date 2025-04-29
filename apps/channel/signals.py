from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from apps.channel.domain.services.notification import NotificationService
from apps.channel.models.notification import Notification


@receiver(m2m_changed, sender=Notification.users.through)
def notification_users_changed(sender, instance: Notification, action, **kwargs):
    if action == "post_add":
        NotificationService.send_notification_on_channels([instance])
