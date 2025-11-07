from django.http import HttpRequest
from django_model_suite.admin import FieldPermissions

from apps.users.models.provider import Provider

from .context import ProviderContextLogic


class BaseProviderPermissions:
    def get_field_rules(
        self, request: HttpRequest, provider: Provider | None = None
    ) -> dict:
        context = ProviderContextLogic(request, provider)
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
            "email": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "company_name": FieldPermissions(
                visible=(context.is_staff),
                editable=(context.is_staff),
            ),
            "user": FieldPermissions(
                visible=(context.is_staff),
                editable=(),
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
