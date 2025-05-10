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
    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        context["show_save"] = False
        return super().render_change_form(request, context, add, change, form_url, obj)
