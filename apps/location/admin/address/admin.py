from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import CSV
from unfold.contrib.import_export.forms import ExportForm

from apps.location.admin.address.form import AddressForm
from apps.location.models.address import Address
from common.base.admin import BaseModelAdmin

from .change_view import AddressChangeView
from .display import AddressDisplayMixin
from .list_view import AddressListView
from .permissions import AddressAdminPermissions
from .resource import AddressResource


@admin.register(Address)
class AddressAdmin(
    AddressDisplayMixin,
    AddressListView,
    AddressChangeView,
    AddressAdminPermissions,
    ExportActionModelAdmin,
    BaseModelAdmin,
):
    resource_class = AddressResource
    export_form_class = ExportForm
    formats = [CSV]
    inlines = []
    form = AddressForm
