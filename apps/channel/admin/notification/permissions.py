from django.http import HttpRequest
from django_model_suite.admin import FieldPermissions

from apps.channel.models.notification import Notification
from common.base.admin import AdminContextLogic

from ...fields.notification import NotificationFields


class BaseNotificationPermissions:
    def get_field_rules(
        self, request: HttpRequest, notification: Notification | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)
        is_created = AdminContextLogic.is_object_created(notification)

        return {
            NotificationFields.NOTIFICATION_TYPE: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            NotificationFields.TITLE: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            NotificationFields.TITLE_AR: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            NotificationFields.TITLE_EN: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            NotificationFields.MESSAGE_BODY: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            NotificationFields.MESSAGE_BODY_AR: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            NotificationFields.MESSAGE_BODY_EN: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            NotificationFields.CREATED_AT: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            NotificationFields.USERS: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            NotificationFields.SEND_SMS: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            NotificationFields.SEND_FCM: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            NotificationFields.IS_READ: FieldPermissions(
                visible=(normal_admin and not is_created),
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
