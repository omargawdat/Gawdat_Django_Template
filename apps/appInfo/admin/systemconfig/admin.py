from django.contrib import admin
from solo.admin import SingletonModelAdmin
from unfold.admin import ModelAdmin

from apps.appInfo.models.system_config import SystemConfig

from .change_view import SystemConfigChangeView


@admin.register(SystemConfig)
class SystemConfigAdmin(
    SystemConfigChangeView,
    ModelAdmin,
    SingletonModelAdmin,
):
    pass
