from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.appInfo.models.faq import FAQ

from .chanage_view import FAQChangeView


@admin.register(FAQ)
class FAQAdmin(
    FAQChangeView,
    ModelAdmin,
    TabbedTranslationAdmin,
):
    pass
