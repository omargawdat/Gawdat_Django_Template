from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.admin import SingletonModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from apps.appInfo.models.app_info import AppInfo


@admin.register(AppInfo)
class AppInfoAdmin(ModelAdmin, SingletonModelAdmin):
    filter_horizontal = ()
    autocomplete_fields = ()
    fieldsets = (
        (
            _("Organizational Overview"),
            {
                "fields": (("about_us_ar", "about_us_en"),),
            },
        ),
        (
            _("Terms"),
            {
                "fields": (("terms_ar", "terms_en"),),
            },
        ),
        (
            _("Policy"),
            {
                "fields": (("policy_ar", "policy_en"),),
            },
        ),
    )
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        context["show_save"] = False
        return super().render_change_form(request, context, add, change, form_url, obj)
