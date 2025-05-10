from django.db.models import QuerySet

from apps.channel.models.notification import Notification
from apps.users.models import User


class NotificationSelector:
    @staticmethod
    def get_notifications_by_user(user: User) -> QuerySet:
        return Notification.objects.filter(users=user)
