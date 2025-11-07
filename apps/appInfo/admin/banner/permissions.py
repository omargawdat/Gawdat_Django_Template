from django.http import HttpRequest

from apps.appInfo.models.banner import Banner
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions


class BaseBannerPermissions:
    def get_field_rules(
        self, request: HttpRequest, banner: Banner | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            "image": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "group": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "is_active": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
        }


class BannerAdminPermissions(BaseBannerPermissions):
    def can_add(self, request, obj=None):
        return True

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return True


class BannerInlinePermissions(BaseBannerPermissions):
    def can_add(self, request, obj=None):
        return True

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return True
