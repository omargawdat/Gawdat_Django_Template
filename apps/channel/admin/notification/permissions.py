from django.http import HttpRequest

from apps.channel.models.notification import Notification
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions


class BaseNotificationPermissions:
    def get_field_config(
        self, request: HttpRequest, notification: Notification | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            "notification_type": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "title": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "title_ar": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "title_en": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "message_body": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "message_body_ar": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "message_body_en": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "created_at": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "users": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "send_sms": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "send_fcm": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "is_read": FieldPermissions(
                visible=(),
                editable=(),
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
