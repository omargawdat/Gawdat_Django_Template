from django.http import HttpRequest
from django_model_suite.admin import FieldPermissions

from apps.location.fields.region import RegionFields
from apps.location.models.region import Region

from .context import RegionContextLogic


class BaseRegionPermissions:
    def get_field_rules(
        self, request: HttpRequest, region: Region | None = None
    ) -> dict:
        context = RegionContextLogic(request, region)

        return {
            RegionFields.CODE: FieldPermissions(
                visible=(context.is_superuser),
                editable=(),
            ),
            RegionFields.COUNTRY: FieldPermissions(
                visible=(context.is_superuser),
                editable=(),
            ),
            RegionFields.GEOMETRY: FieldPermissions(
                visible=(context.is_superuser),
                editable=(),
            ),
            RegionFields.NAME_AR: FieldPermissions(
                visible=(context.is_superuser),
                editable=(context.is_superuser),
            ),
            RegionFields.NAME_EN: FieldPermissions(
                visible=(context.is_superuser),
                editable=(context.is_superuser),
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
