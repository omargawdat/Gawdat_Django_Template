from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import register

from apps.appInfo.models.app_info import AppInfo
from apps.appInfo.models.faq import FAQ


@register(AppInfo)
class AppInfoTranslationOptions(TranslationOptions):
    fields = ("about_us", "terms", "policy")


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ("question", "answer")
