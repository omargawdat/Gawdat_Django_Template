from django.http import HttpRequest
from django_model_suite.admin import FieldPermissions

from apps.location.fields.country import CountryFields
from apps.location.models.country import Country

from .context import CountryContextLogic


class BaseCountryPermissions:
    def get_field_rules(
        self, request: HttpRequest, country: Country | None = None
    ) -> dict:
        context = CountryContextLogic(request, country)

        return {
            CountryFields.CODE: FieldPermissions(
                visible=(context.is_staff,),
                editable=(),
            ),
            CountryFields.CURRENCY: FieldPermissions(
                visible=(context.is_staff,),
                editable=(),
            ),
            CountryFields.NAME: FieldPermissions(
                visible=(context.is_staff,),
                editable=(context.is_staff,),
            ),
            CountryFields.NAME_AR: FieldPermissions(
                visible=(context.is_staff,),
                editable=(context.is_staff,),
            ),
            CountryFields.NAME_EN: FieldPermissions(
                visible=(context.is_staff,),
                editable=(),
            ),
            CountryFields.PHONE_CODE: FieldPermissions(
                visible=(context.is_staff,),
                editable=(context.is_staff,),
            ),
            CountryFields.FLAG: FieldPermissions(
                visible=(context.is_staff,),
                editable=(context.is_staff,),
            ),
            CountryFields.IS_ACTIVE: FieldPermissions(
                visible=(context.is_staff,),
                editable=(context.is_staff,),
            ),
        }


class CountryAdminPermissions(BaseCountryPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return False


class CountryInlinePermissions(BaseCountryPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
