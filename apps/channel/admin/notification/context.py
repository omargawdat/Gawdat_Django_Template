from django.http import HttpRequest

from apps.channel.models.notification import Notification


class NotificationContextLogic:
    def __init__(self, request: HttpRequest, notification: Notification | None = None):
        self.request = request
        self.notification = notification

    @property
    def is_superuser(self) -> bool:
        return self.request.user.is_superuser

    @property
    def is_staff(self) -> bool:
        return self.request.user.is_staff

    @property
    def is_creating(self) -> bool:
        return self.notification is None
