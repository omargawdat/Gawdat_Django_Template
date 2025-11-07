from django.http import HttpRequest

from apps.location.models.country import Country
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions


class BaseCountryPermissions:
    def get_field_rules(
        self, request: HttpRequest, country: Country | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            "code": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "name": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "name_ar": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "name_en": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "currency": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "flag": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "is_active": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "phone_code": FieldPermissions(
                visible=(normal_admin),
                editable=(),
            ),
            "app_install_money_invitee": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "app_install_money_inviter": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "order_money_invitee": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "order_money_inviter": FieldPermissions(
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
