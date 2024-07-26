from django.contrib import admin
from django.db import models
from solo.admin import SingletonModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from apps.appInfo.models.terms import TermsAndConditions


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(SingletonModelAdmin, ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
