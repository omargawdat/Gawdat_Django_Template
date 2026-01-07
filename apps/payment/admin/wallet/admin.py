from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import XLSX
from unfold.contrib.import_export.forms import ExportForm

from apps.payment.domain.selectors.wallet import WalletSelector
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
    ExportActionModelAdmin,
    BaseModelAdmin,
):
    resource_class = WalletResource
    export_form_class = ExportForm
    formats = [XLSX]
    change_list_template = "admin/payment/wallet/change_list.html"
    import_export_change_list_template = "admin/payment/wallet/change_list.html"

    def changelist_view(self, request, extra_context=None):
        total_balance = WalletSelector.get_total_balance()
        avg_balance = WalletSelector.get_average_balance()
        wallet_usage = WalletSelector.get_wallet_usage_rate()
        active_wallets = WalletSelector.get_active_wallets_count()

        cards = [
            {
                "title": _("Total Balance"),
                "value": total_balance,
                "description": _("Sum of all wallet balances"),
            },
            {
                "title": _("Avg Balance"),
                "value": avg_balance,
                "description": _("Average balance per wallet"),
            },
            {
                "title": _("Wallet Usage"),
                "value": wallet_usage,
                "description": _("Wallets enabled for payments"),
            },
            {
                "title": _("Active Wallets"),
                "value": active_wallets,
                "description": _("Wallets with balance > 0"),
            },
        ]

        extra_context = extra_context or {}
        extra_context.update({"wallet_cards": cards})
        return super().changelist_view(request, extra_context=extra_context)
