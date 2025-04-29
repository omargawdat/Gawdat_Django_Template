import logging

from django.db.models import QuerySet
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message
from firebase_admin.messaging import Notification as FCMNotification

logger = logging.getLogger(__name__)


class FcmUtils:
    @staticmethod
    def send_notification(
        *,
        title: str,
        message_body: str,
        data: dict[str, str],
        devices: QuerySet[FCMDevice],
    ) -> None:
        fcm_message = Message(
            notification=FCMNotification(title=title, body=message_body), data=data
        )

        try:
            devices.send_message(fcm_message)
            logger.info("Successfully sent FCM message to %s devices", devices.count())
        except Exception:
            logger.exception("Error sending bulk FCM messages")
