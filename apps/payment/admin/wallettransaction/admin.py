from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import XLSX
from unfold.contrib.import_export.forms import ExportForm

from apps.payment.domain.selectors.wallet_transactions import WalletTransactionSelector
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
    formats = [XLSX]
    change_list_template = "admin/payment/wallettransaction/change_list.html"
    import_export_change_list_template = (
        "admin/payment/wallettransaction/change_list.html"
    )

    def changelist_view(self, request, extra_context=None):
        transactions_today = WalletTransactionSelector.get_transactions_today()
        money_added = WalletTransactionSelector.get_money_added_today()
        money_deducted = WalletTransactionSelector.get_money_deducted_today()
        net_change = WalletTransactionSelector.get_net_change_today()

        cards = [
            {
                "title": _("Transactions Today"),
                "value": transactions_today,
                "description": _("Total transactions created today"),
            },
            {
                "title": _("Money Added"),
                "value": money_added,
                "description": _("Credits added to wallets today"),
            },
            {
                "title": _("Money Deducted"),
                "value": money_deducted,
                "description": _("Debits from wallets today"),
            },
            {
                "title": _("Net Change"),
                "value": net_change,
                "description": _("Net wallet balance change today"),
            },
        ]

        extra_context = extra_context or {}
        extra_context.update({"transaction_cards": cards})
        return super().changelist_view(request, extra_context=extra_context)
