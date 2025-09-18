from django.http import HttpRequest

from apps.location.models.country import Country
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions

from ...fields.country import CountryFields


class BaseCountryPermissions:
    def get_field_rules(
        self, request: HttpRequest, country: Country | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            CountryFields.CODE: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            CountryFields.NAME: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            CountryFields.NAME_AR: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            CountryFields.NAME_EN: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            CountryFields.CURRENCY: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            CountryFields.FLAG: FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            CountryFields.IS_ACTIVE: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            CountryFields.PHONE_CODE: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
        }


class CountryAdminPermissions(BaseCountryPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return True


class CountryInlinePermissions(BaseCountryPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
