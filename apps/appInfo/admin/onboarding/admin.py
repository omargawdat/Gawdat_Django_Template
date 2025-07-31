from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.appInfo.models.onboarding import Onboarding
from common.base.admin import BaseModelAdmin

from .change_view import OnboardingChangeView
from .display import OnboardingDisplayMixin
from .list_view import OnboardingListView
from .permissions import OnboardingAdminPermissions


@admin.register(Onboarding)
class OnboardingAdmin(
    OnboardingDisplayMixin,
    OnboardingListView,
    OnboardingChangeView,
    OnboardingAdminPermissions,
    BaseModelAdmin,
    TabbedTranslationAdmin,
):
    inlines = []
