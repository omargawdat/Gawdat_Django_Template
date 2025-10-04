from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import register

from apps.location.models.country import Country
from apps.location.models.region import Region


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ()  # name is now a property, not a field
