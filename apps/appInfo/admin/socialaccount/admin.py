from django.contrib import admin
from solo.admin import SingletonModelAdmin
from unfold.admin import ModelAdmin

from apps.appInfo.models.social import SocialAccount

from .change_view import SocialAccountChangeView


@admin.register(SocialAccount)
class SocialAccountAdmin(
    SocialAccountChangeView,
    ModelAdmin,
    SingletonModelAdmin,
):
    pass
