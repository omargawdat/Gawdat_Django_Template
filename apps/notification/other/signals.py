from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message
from firebase_admin.messaging import Notification as FCMNotification

from apps.notification.models.notification import Notification


@receiver(m2m_changed, sender=Notification.users.through)
def push_notification(sender, instance: Notification, action, **kwargs):
    if action == "post_add":
        fcm_message = Message(
            notification=FCMNotification(
                title=instance.title,
                body=instance.message_body,
            ),
            data={
                "notification_id": str(instance.id),
                "notification_type": str(instance.notification_type),
                "created_at": str(instance.created_at.isoformat()),
            },
        )
        devices = FCMDevice.objects.filter(user__in=instance.users.all())
        if devices:
            devices_list = list(devices)
            batch_size = 1000  # firebase has a limit of 1000 devices per batch
            for i in range(0, len(devices_list), batch_size):
                batch = devices_list[i : i + batch_size]
                FCMDevice.objects.filter(
                    id__in=[device.id for device in batch],
                ).send_message(
                    fcm_message,
                )
