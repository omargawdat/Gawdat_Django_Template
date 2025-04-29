from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import CSV
from unfold.contrib.import_export.forms import ExportForm

from apps.products.models.brand import Brand
from common.base.admin import BaseModelAdmin

from .change_view import BrandChangeView
from .display import BrandDisplayMixin
from .list_view import BrandListView
from .permissions import BrandAdminPermissions
from .resource import BrandResource


@admin.register(Brand)
class BrandAdmin(
    BrandDisplayMixin,
    BrandListView,
    BrandChangeView,
    BrandAdminPermissions,
    ExportActionModelAdmin,
    BaseModelAdmin,
):
    resource_class = BrandResource
    export_form_class = ExportForm
    formats = [CSV]
    inlines = []
