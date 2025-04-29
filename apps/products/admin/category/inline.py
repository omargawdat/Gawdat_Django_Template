from apps.products.models.category import Category
from common.base.admin import BaseTabularInline

from .permissions import CategoryInlinePermissions


class CategoryInline(CategoryInlinePermissions, BaseTabularInline):
    model = Category
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
