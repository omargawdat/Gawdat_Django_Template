from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from solo.admin import SingletonModelAdmin
from unfold.admin import ModelAdmin

from apps.appInfo.models.social import SocialAccount


@admin.register(SocialAccount)
class SocialAccountsAdmin(SingletonModelAdmin, ModelAdmin):
    fieldsets = (
        (
            _("Social Media Accounts"),
            {
                "fields": ("twitter", "instagram", "tiktok", "website"),
            },
        ),
        (
            _("Contact Information"),
            {
                "fields": ("email", "phone_number"),
            },
        ),
    )
