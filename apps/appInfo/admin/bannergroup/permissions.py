from django.http import HttpRequest

from apps.appInfo.models.banner_group import BannerGroup
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions


class BaseBannerGroupPermissions:
    def get_field_config(
        self, request: HttpRequest, banner_group: BannerGroup | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            "name": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "name_ar": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "name_en": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "order": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "is_active": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
        }


class BannerGroupAdminPermissions(BaseBannerGroupPermissions):
    def can_add(self, request, obj=None):
        return True

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return True


class BannerGroupInlinePermissions(BaseBannerGroupPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
