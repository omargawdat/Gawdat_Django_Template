from django.http import HttpRequest

from apps.appInfo.models.onboarding import Onboarding
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions

from ...fields.onboarding import OnboardingFields


class BaseOnboardingPermissions:
    def get_field_rules(
        self, request: HttpRequest, onboarding: Onboarding | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            OnboardingFields.TITLE: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            OnboardingFields.TITLE_AR: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            OnboardingFields.TITLE_EN: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            OnboardingFields.IMAGE: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            OnboardingFields.TEXT: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            OnboardingFields.TEXT_AR: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            OnboardingFields.TEXT_EN: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            OnboardingFields.SUB_TEXT: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            OnboardingFields.SUB_TEXT_EN: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            OnboardingFields.SUB_TEXT_AR: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            OnboardingFields.ORDER: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            OnboardingFields.IS_ACTIVE: FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
        }


class OnboardingAdminPermissions(BaseOnboardingPermissions):
    def can_add(self, request, obj=None):
        return True

    def can_change(self, request, obj=None):
        return True

    def can_delete(self, request, obj=None):
        return True


class OnboardingInlinePermissions(BaseOnboardingPermissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
