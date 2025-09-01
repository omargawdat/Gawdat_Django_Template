from django.http import HttpRequest
from django_model_suite.admin import FieldPermissions

from apps.users.fields.customer import CustomerFields
from apps.users.models.customer import Customer

from .context import CustomerContextLogic


class BaseCustomerPermissions:
    def get_field_rules(
        self, request: HttpRequest, customer: Customer | None = None
    ) -> dict:
        context = CustomerContextLogic(request, customer)

        return {
            CustomerFields.IS_SUPERUSER: FieldPermissions(
                visible=(context.is_staff),
                editable=(),
            ),
            CustomerFields.USERNAME: FieldPermissions(
                visible=(context.is_staff),
                editable=(),
            ),
            CustomerFields.IS_ACTIVE: FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(context.is_staff,),
            ),
            CustomerFields.DATE_JOINED: FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(),
            ),
            CustomerFields.PHONE_NUMBER: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff and not context.is_created),
            ),
            CustomerFields.EMAIL: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            CustomerFields.IMAGE: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            CustomerFields.FULL_NAME: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            CustomerFields.GENDER: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            CustomerFields.BIRTH_DATE: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            CustomerFields.COUNTRY: FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(),
            ),
            CustomerFields.PRIMARY_ADDRESS: FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(),
            ),
            CustomerFields.REFERRAL_CUSTOMER_ID: FieldPermissions(
                visible=(context.is_staff and context.is_created), editable=()
            ),
        }


class CustomerAdminPermissions(BaseCustomerPermissions):
    def can_add(self, request, obj=None):
        return True  # todo: can't add user as is should call the create action from services

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
