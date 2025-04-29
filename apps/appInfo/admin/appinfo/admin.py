from django.contrib import admin
from solo.admin import SingletonModelAdmin
from unfold.admin import ModelAdmin

from apps.appInfo.models.app_info import AppInfo

from .change_view import AppInfoChangeView


@admin.register(AppInfo)
class AppInfoAdmin(
    AppInfoChangeView,
    ModelAdmin,
    SingletonModelAdmin,
):
    pass
