from django.http import HttpRequest

from apps.users.models.admin import AdminUser
from common.base.admin import FieldPermissions

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

    def get_field_config(
        self, request: HttpRequest, admin_user: AdminUser | None = None
    ) -> dict:
        context = AdminUserContextLogic(request, admin_user)

        return {
            "password": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "last_login": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "is_superuser": FieldPermissions(
                visible=(),
                editable=(),
            ),
            "is_active": FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(context.is_staff and context.is_created),
            ),
            "is_staff": FieldPermissions(
                visible=(context.is_staff),
                editable=(),
            ),
            "date_joined": FieldPermissions(
                visible=(context.is_staff),
                editable=(),
            ),
            "groups": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "user_permissions": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "language": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "image": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "can_access_money": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
        }
