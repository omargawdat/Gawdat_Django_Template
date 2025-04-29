from django.http import HttpRequest

from apps.products.models.brand import Brand
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions

from ...fields.brand import BrandFields


class BaseBrandPermissions:
    def get_field_rules(self, request: HttpRequest, brand: Brand | None = None) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            BrandFields.LOGO: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            BrandFields.NAME: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
        }


class BrandAdminPermissions(BaseBrandPermissions):
    def can_add(self, request, obj=None):
        return True

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return True


class BrandInlinePermissions(BaseBrandPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
