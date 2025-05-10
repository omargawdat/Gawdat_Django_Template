from apps.products.models.brand import Brand
from common.base.admin import BaseTabularInline

from .permissions import BrandInlinePermissions


class BrandInline(BrandInlinePermissions, BaseTabularInline):
    model = Brand
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
