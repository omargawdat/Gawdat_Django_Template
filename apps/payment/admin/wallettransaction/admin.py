from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import CSV
from unfold.contrib.import_export.forms import ExportForm

from apps.payment.models.wallet_transaction import WalletTransaction
from common.base.admin import BaseModelAdmin

from .change_view import WalletTransactionChangeView
from .display import WalletTransactionDisplayMixin
from .list_view import WalletTransactionListView
from .permissions import WalletTransactionAdminPermissions
from .resource import WalletTransactionResource


@admin.register(WalletTransaction)
class WalletTransactionAdmin(
    WalletTransactionDisplayMixin,
    WalletTransactionListView,
    WalletTransactionChangeView,
    WalletTransactionAdminPermissions,
    ExportActionModelAdmin,
    BaseModelAdmin,
):
    resource_class = WalletTransactionResource
    export_form_class = ExportForm
    formats = [CSV]
