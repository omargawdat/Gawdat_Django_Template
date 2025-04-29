from django.http import HttpRequest

from apps.location.models.address import Address
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions

from ...fields.address import AddressFields


class BaseAddressPermissions:
    def get_field_rules(
        self, request: HttpRequest, address: Address | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            AddressFields.CUSTOMER: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            AddressFields.POINT: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            AddressFields.DESCRIPTION: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            AddressFields.LOCATION_TYPE: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
        }


class AddressAdminPermissions(BaseAddressPermissions):
    def can_add(self, request, obj=None):
        return True

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return True


class AddressInlinePermissions(BaseAddressPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
