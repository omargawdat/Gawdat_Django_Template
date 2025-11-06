from django.http import HttpRequest
from django_model_suite.admin import FieldPermissions

from apps.users.fields.provider import ProviderFields
from apps.users.models.provider import Provider

from .context import ProviderContextLogic


class BaseProviderPermissions:
    def get_field_rules(
        self, request: HttpRequest, provider: Provider | None = None
    ) -> dict:
        context = ProviderContextLogic(request, provider)
        return {
            ProviderFields.IS_SUPERUSER: FieldPermissions(
                visible=(context.is_staff),
                editable=(),
            ),
            ProviderFields.IS_ACTIVE: FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(context.is_staff,),
            ),
            ProviderFields.DATE_JOINED: FieldPermissions(
                visible=(context.is_staff and context.is_created),
                editable=(),
            ),
            ProviderFields.EMAIL: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            ProviderFields.COMPANY_NAME: FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
        }


class ProviderAdminPermissions(BaseProviderPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return False


class ProviderInlinePermissions(BaseProviderPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
