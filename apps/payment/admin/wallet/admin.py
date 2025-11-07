from django.contrib import admin
from import_export.formats.base_formats import CSV
from unfold.contrib.import_export.forms import ExportForm

from apps.payment.models.wallet import Wallet
from common.base.admin import BaseModelAdmin

from .change_view import WalletChangeView
from .display import WalletDisplayMixin
from .list_view import WalletListView
from .permissions import WalletAdminPermissions
from .resource import WalletResource


@admin.register(Wallet)
class WalletAdmin(
    WalletDisplayMixin,
    WalletListView,
    WalletChangeView,
    WalletAdminPermissions,
    BaseModelAdmin,
):
    resource_class = WalletResource
    export_form_class = ExportForm
    formats = [CSV]
