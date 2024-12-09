import logging
from collections import defaultdict

from apps.notification.models.notification import Notification
from apps.notification.other.constants import NOTIFICATION_MESSAGES
from apps.notification.other.constants import NotificationTypes
from apps.users.models import User

logger = logging.getLogger(__name__)


class NotificationService:
    @staticmethod
    def create_notification(
        notification_type: NotificationTypes,
        users: list[User] | None = None,
    ) -> None:
        users = [user for user in users if user]  # remove null if any.

        language_grouped_users = defaultdict(list)
        for user in users:
            language_grouped_users[user.picked_language].append(user)

        for lang, users_in_lang in language_grouped_users.items():
            notification_messages = NOTIFICATION_MESSAGES.get(
                notification_type.value,
                {},
            ).get(
                lang,
                {},
            )
            title = notification_messages.get("title", "Notification")
            message_body = notification_messages.get(
                "body",
                "You have a new notification.",
            )
            notification = Notification.objects.create(
                notification_type=notification_type.value,
                title=title,
                message_body=message_body,
            )
            notification.users.add(*users_in_lang)
