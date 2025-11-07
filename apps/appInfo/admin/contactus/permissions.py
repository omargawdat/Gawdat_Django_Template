from django.http import HttpRequest

from apps.appInfo.models.contact_us import ContactUs
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions


class BaseContactUsPermissions:
    def get_field_rules(
        self, request: HttpRequest, contact_us: ContactUs | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            "customer": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "contact_type": FieldPermissions(
                visible=(),
                editable=(),
            ),
            "description": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "has_checked": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "created_at": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
        }


class ContactUsAdminPermissions(BaseContactUsPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return False


class ContactUsInlinePermissions(BaseContactUsPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
