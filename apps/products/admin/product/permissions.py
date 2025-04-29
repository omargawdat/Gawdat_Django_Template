from django.http import HttpRequest

from apps.products.models.product import Product
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions

from ...fields.product import ProductFields


class BaseProductPermissions:
    def get_field_rules(
        self, request: HttpRequest, product: Product | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            ProductFields.NAME: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            ProductFields.DESCRIPTION: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            ProductFields.PRICE_CURRENCY: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            ProductFields.PRICE: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            ProductFields.IMAGE: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            ProductFields.CATEGORY: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            ProductFields.NAME_AR: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            ProductFields.NAME_EN: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
        }


class ProductAdminPermissions(BaseProductPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False


class ProductInlinePermissions(BaseProductPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
