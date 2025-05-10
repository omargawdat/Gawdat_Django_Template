from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import CSV
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.contrib.import_export.forms import ExportForm

from apps.products.models.category import Category
from common.base.admin import BaseModelAdmin

from .change_view import CategoryChangeView
from .display import CategoryDisplayMixin
from .list_view import CategoryListView
from .permissions import CategoryAdminPermissions
from .resource import CategoryResource


@admin.register(Category)
class CategoryAdmin(
    CategoryDisplayMixin,
    CategoryListView,
    CategoryChangeView,
    CategoryAdminPermissions,
    ExportActionModelAdmin,
    BaseModelAdmin,
    TabbedTranslationAdmin,
):
    resource_class = CategoryResource
    export_form_class = ExportForm
    formats = [CSV]
    inlines = []
