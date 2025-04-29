from django.http import HttpRequest

from apps.products.models.category import Category
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions

from ...fields.category import CategoryFields


class BaseCategoryPermissions:
    def get_field_rules(
        self, request: HttpRequest, category: Category | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            CategoryFields.NAME: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            CategoryFields.IMAGE: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            CategoryFields.NAME_AR: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            CategoryFields.NAME_EN: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
        }


class CategoryAdminPermissions(BaseCategoryPermissions):
    def can_add(self, request, obj=None):
        return True

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return True


class CategoryInlinePermissions(BaseCategoryPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
