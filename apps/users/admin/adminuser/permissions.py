from django.http import HttpRequest

from apps.users.models.admin import AdminUser
from common.base.admin import FieldPermissions

from ...fields.admin_user import AdminUserFields
from .context import AdminUserContextLogic


class AdminUserPermissions:
    def can_add(self, request: HttpRequest) -> bool:
        return True

    def can_change(
        self, request: HttpRequest, admin_user: AdminUser | None = None
    ) -> bool:
        return True

    def can_delete(
        self, request: HttpRequest, admin_user: AdminUser | None = None
    ) -> bool:
        return False

    def get_field_rules(
        self, request: HttpRequest, admin_user: AdminUser | None = None
    ) -> dict:
        context = AdminUserContextLogic(request, admin_user)

        return {
            AdminUserFields.PASSWORD: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            AdminUserFields.LAST_LOGIN: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            AdminUserFields.IS_SUPERUSER: FieldPermissions(
                visible=(),
                editable=(),
            ),
            AdminUserFields.POLYMORPHIC_CTYPE: FieldPermissions(
                visible=(context.is_staff),
                editable=(),
            ),
            AdminUserFields.USERNAME: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            AdminUserFields.IS_ACTIVE: FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(context.is_staff and context.is_created),
            ),
            AdminUserFields.IS_STAFF: FieldPermissions(
                visible=(context.is_staff),
                editable=(),
            ),
            AdminUserFields.DATE_JOINED: FieldPermissions(
                visible=(context.is_staff),
                editable=(),
            ),
            AdminUserFields.GROUPS: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            AdminUserFields.USER_PERMISSIONS: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            AdminUserFields.LANGUAGE: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            AdminUserFields.IMAGE: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            AdminUserFields.CAN_ACCESS_MONEY: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
        }
