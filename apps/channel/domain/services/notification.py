import logging
from typing import Any

from django.contrib.auth import get_user_model

from apps.channel.constants import NotificationType
from apps.channel.domain.services.device import DeviceService
from apps.channel.domain.utilities.fcm import FcmUtils
from apps.channel.domain.utilities.sms import SMSUtils
from apps.channel.models.notification import Notification
from apps.channel.template_message import notification_templates
from apps.users.domain.selectors.user import UserSelector

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class NotificationService:
    @staticmethod
    def create_action_notifications(
        *,
        users: list[UserModel],
        notification_type: NotificationType,
        object_id: int | None = None,
        send_sms: bool = False,
        send_fcm: bool = False,
        **kwargs: Any,
    ):
        try:
            user_groups = UserSelector.group_users_by_type(users)
            for user_type, user_list in user_groups.items():
                title = NotificationType(notification_type).label
                body_template = notification_templates[notification_type][user_type]
                title_str = str(title)
                body = str(body_template).format(**kwargs)
                notification = Notification.objects.create(
                    notification_type=notification_type,
                    object_id=object_id,
                    send_sms=send_sms,
                    send_fcm=send_fcm,
                    title=title_str,
                    message_body=body,
                )
                notification.users.add(*user_list)
        except Exception:
            logger.exception("Error creating notifications")

    @staticmethod
    def send_notification_on_channels(
        notifications: list[Notification],
    ) -> None:
        for notification in notifications:
            title = notification.title
            body = notification.message_body
            data = {}

            users_by_language = UserSelector.group_by_language(notification.users.all())
            for users in users_by_language.values():
                if notification.send_fcm:
                    active_devices = DeviceService.get_active_devices_for_users(users)

                    if active_devices:
                        FcmUtils.send_notification(
                            title=title,
                            message_body=body,
                            data=data,
                            devices=active_devices,
                        )

                if notification.send_sms:
                    SMSUtils.send_bulk_message(
                        phone_numbers=[user.phone_number for user in users],
                        message=body,
                    )
