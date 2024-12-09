from django.contrib import admin
from django.db import models
from solo.admin import SingletonModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from apps.appInfo.models.about import AboutUs


@admin.register(AboutUs)
class AboutUsAdmin(SingletonModelAdmin, ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }
