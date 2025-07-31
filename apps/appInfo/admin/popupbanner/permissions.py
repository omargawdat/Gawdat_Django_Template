from django.http import HttpRequest

from apps.appInfo.models.popup import PopUpBanner
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions

from ...fields.pop_up_banner import PopUpBannerFields


class BasePopUpBannerPermissions:
    def get_field_rules(
        self, request: HttpRequest, pop_up_banner: PopUpBanner | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            PopUpBannerFields.IMAGE: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            PopUpBannerFields.COUNT_PER_USER: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            PopUpBannerFields.IS_ACTIVE: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
        }


class PopUpBannerAdminPermissions(BasePopUpBannerPermissions):
    def can_add(self, request, obj=None):
        return True

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return True


class PopUpBannerInlinePermissions(BasePopUpBannerPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
