from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import CSV
from unfold.contrib.import_export.forms import ExportForm

from apps.products.models.banner import Banner
from common.base.admin import BaseModelAdmin

from .change_view import BannerChangeView
from .display import BannerDisplayMixin
from .list_view import BannerListView
from .permissions import BannerAdminPermissions
from .resource import BannerResource


@admin.register(Banner)
class BannerAdmin(
    BannerDisplayMixin,
    BannerListView,
    BannerChangeView,
    BannerAdminPermissions,
    ExportActionModelAdmin,
    BaseModelAdmin,
):
    resource_class = BannerResource
    export_form_class = ExportForm
    formats = [CSV]
    inlines = []
