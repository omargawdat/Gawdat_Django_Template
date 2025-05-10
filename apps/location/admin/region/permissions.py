from django.http import HttpRequest
from django_model_suite.admin import FieldPermissions

from apps.location.fields.region import RegionFields
from apps.location.models.region import Region
from common.base.admin import AdminContextLogic


class BaseRegionPermissions:
    def get_field_rules(
        self, request: HttpRequest, region: Region | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            RegionFields.CODE: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            RegionFields.COUNTRY: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            RegionFields.GEOMETRY: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            RegionFields.NAME_AR: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            RegionFields.NAME_EN: FieldPermissions(
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
