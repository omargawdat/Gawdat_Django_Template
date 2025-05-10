from apps.products.models.product import Product
from common.base.admin import BaseTabularInline

from .permissions import ProductInlinePermissions


class ProductInline(ProductInlinePermissions, BaseTabularInline):
    model = Product
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
