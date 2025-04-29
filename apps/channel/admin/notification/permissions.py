from django.http import HttpRequest
from django_model_suite.admin import FieldPermissions

from apps.channel.models.notification import Notification

from ...fields.notification import NotificationFields
from .context import NotificationContextLogic


class BaseNotificationPermissions:
    def get_field_rules(
        self, request: HttpRequest, notification: Notification | None = None
    ) -> dict:
        context = NotificationContextLogic(request, notification)

        return {
            NotificationFields.NOTIFICATION_TYPE: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            NotificationFields.TITLE: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            NotificationFields.MESSAGE_BODY: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            NotificationFields.CREATED_AT: FieldPermissions(
                visible=(context.is_staff),
                editable=(),
            ),
            NotificationFields.USERS: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
        }


class NotificationAdminPermissions(BaseNotificationPermissions):
    def can_add(self, request, obj=None):
        return True

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return True


class NotificationInlinePermissions(BaseNotificationPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
