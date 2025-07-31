from apps.appInfo.models.onboarding import Onboarding
from common.base.admin import BaseTabularInline

from .permissions import OnboardingInlinePermissions


class OnboardingInline(OnboardingInlinePermissions, BaseTabularInline):
    model = Onboarding
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
