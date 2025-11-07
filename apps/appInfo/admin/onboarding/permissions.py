from django.http import HttpRequest

from apps.appInfo.models.onboarding import Onboarding
from common.base.admin import AdminContextLogic
from common.base.admin import FieldPermissions


class BaseOnboardingPermissions:
    def get_field_config(
        self, request: HttpRequest, onboarding: Onboarding | None = None
    ) -> dict:
        normal_admin = AdminContextLogic.is_normal_admin(request)

        return {
            "title": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "title_ar": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "title_en": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "image": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "text": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "text_ar": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "text_en": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "sub_text": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "sub_text_en": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "sub_text_ar": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "order": FieldPermissions(
                visible=(normal_admin),
                editable=(normal_admin),
            ),
            "is_active": FieldPermissions(
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
