from django.http import HttpRequest

from apps.location.models.region import Region
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions


class BaseRegionPermissions:
    def get_field_rules(
        self, request: HttpRequest, region: Region | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            "code": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "country": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "geometry": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "name_ar": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "name_en": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
        }


class RegionAdminPermissions(BaseRegionPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return False


class RegionInlinePermissions(BaseRegionPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
