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
            CustomerFields.PASSWORD: FieldPermissions(
                visible=(context.is_superuser),
                editable=(context.is_superuser),
            ),
            CustomerFields.LAST_LOGIN: FieldPermissions(
                visible=(context.is_superuser),
                editable=(),
            ),
            CustomerFields.IS_SUPERUSER: FieldPermissions(
                visible=(context.is_superuser),
                editable=(),
            ),
            CustomerFields.POLYMORPHIC_CTYPE: FieldPermissions(
                visible=(context.is_superuser),
                editable=(),
            ),
            CustomerFields.USERNAME: FieldPermissions(
                visible=(context.is_superuser),
                editable=(context.is_superuser),
            ),
            CustomerFields.IS_ACTIVE: FieldPermissions(
                visible=(context.is_superuser and context.is_created),
                editable=(),
            ),
            CustomerFields.IS_STAFF: FieldPermissions(
                visible=(context.is_superuser),
                editable=(),
            ),
            CustomerFields.DATE_JOINED: FieldPermissions(
                visible=(context.is_superuser and context.is_created),
                editable=(),
            ),
            CustomerFields.GROUPS: FieldPermissions(
                visible=(context.is_superuser),
                editable=(),
            ),
            CustomerFields.USER_PERMISSIONS: FieldPermissions(
                visible=(context.is_superuser),
                editable=(),
            ),
            CustomerFields.PHONE_NUMBER: FieldPermissions(
                visible=(context.is_superuser),
                editable=(context.is_superuser),
            ),
            CustomerFields.EMAIL: FieldPermissions(
                visible=(context.is_superuser),
                editable=(context.is_superuser),
            ),
            CustomerFields.IMAGE: FieldPermissions(
                visible=(context.is_superuser),
                editable=(context.is_superuser),
            ),
            CustomerFields.FULL_NAME: FieldPermissions(
                visible=(context.is_superuser),
                editable=(context.is_superuser),
            ),
            CustomerFields.GENDER: FieldPermissions(
                visible=(context.is_superuser),
                editable=(context.is_superuser),
            ),
            CustomerFields.BIRTH_DATE: FieldPermissions(
                visible=(context.is_superuser),
                editable=(context.is_superuser),
            ),
            CustomerFields.COUNTRY: FieldPermissions(
                visible=(context.is_superuser and context.is_created),
                editable=(),
            ),
            CustomerFields.PRIMARY_ADDRESS: FieldPermissions(
                visible=(context.is_superuser),
                editable=(context.is_superuser),
            ),
        }


class CustomerAdminPermissions(BaseCustomerPermissions):
    def can_add(self, request, obj=None):
        return True

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return True


class CustomerInlinePermissions(BaseCustomerPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
