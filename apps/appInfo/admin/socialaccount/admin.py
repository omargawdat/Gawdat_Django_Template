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
    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        context["show_save"] = False
        return super().render_change_form(request, context, add, change, form_url, obj)
