from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import CSV
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.contrib.import_export.forms import ExportForm

from apps.products.models.product import Product
from common.base.admin import BaseModelAdmin

from .change_view import ProductChangeView
from .display import ProductDisplayMixin
from .list_view import ProductListView
from .permissions import ProductAdminPermissions
from .resource import ProductResource


@admin.register(Product)
class ProductAdmin(
    ProductDisplayMixin,
    ProductListView,
    ProductChangeView,
    ProductAdminPermissions,
    ExportActionModelAdmin,
    BaseModelAdmin,
    TabbedTranslationAdmin,
):
    resource_class = ProductResource
    export_form_class = ExportForm
    formats = [CSV]
    inlines = []
