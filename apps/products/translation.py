from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import register

from apps.products.models.category import Category
from apps.products.models.product import Product


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("name",)
