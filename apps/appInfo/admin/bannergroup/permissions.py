from django.http import HttpRequest

from apps.appInfo.models.banner_group import BannerGroup
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions

from ...fields.banner_group import BannerGroupFields


class BaseBannerGroupPermissions:
    def get_field_rules(
        self, request: HttpRequest, banner_group: BannerGroup | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            BannerGroupFields.NAME: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            BannerGroupFields.NAME_AR: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            BannerGroupFields.NAME_EN: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            BannerGroupFields.ORDER: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            BannerGroupFields.IS_ACTIVE: FieldPermissions(
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
