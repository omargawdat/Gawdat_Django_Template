from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import XLSX
from unfold.contrib.import_export.forms import ExportForm

from apps.location.models.country import Country
from common.base.admin import BaseModelAdmin

from .change_view import CountryChangeView
from .display import CountryDisplayMixin
from .list_view import CountryListView
from .permissions import CountryAdminPermissions
from .resource import CountryResource


@admin.register(Country)
class CountryAdmin(
    CountryDisplayMixin,
    CountryListView,
    CountryChangeView,
    CountryAdminPermissions,
    ExportActionModelAdmin,
    BaseModelAdmin,
):
    resource_class = CountryResource
    export_form_class = ExportForm
    formats = [XLSX]
    inlines = []
