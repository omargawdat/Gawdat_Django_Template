from django.http import HttpRequest

from apps.users.models.customer import Customer
from common.base.admin import FieldPermissions

from .context import CustomerContextLogic


class BaseCustomerPermissions:
    def get_field_rules(
        self, request: HttpRequest, customer: Customer | None = None
    ) -> dict:
        context = CustomerContextLogic(request, customer)
        return {
            "is_superuser": FieldPermissions(
                visible=(context.is_staff),
                editable=(),
            ),
            "is_active": FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(context.is_staff,),
            ),
            "date_joined": FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(),
            ),
            "phone_number": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff and not context.is_created),
            ),
            "email": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "image": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "full_name": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "gender": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "birth_date": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "country": FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(),
            ),
            "primary_address": FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(),
            ),
            "is_verified": FieldPermissions(
                visible=(context.is_staff),
                editable=(),
            ),
            "inviter": FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(),
            ),
            "user": FieldPermissions(
                visible=(context.is_staff),
                editable=(),
            ),
        }


class CustomerAdminPermissions(BaseCustomerPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return False


class CustomerInlinePermissions(BaseCustomerPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
