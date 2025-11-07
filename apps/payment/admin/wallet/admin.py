from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import CSV
from unfold.contrib.import_export.forms import ExportForm
from unfold.decorators import action
from unfold.enums import ActionVariant

from apps.payment.admin.wallet.process_transaction_form import WalletTransactionForm
from apps.payment.domain.services.wallet_transaction import WalletTransactionService
from apps.payment.models.wallet import Wallet
from apps.users.models.admin import AdminUser
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
    formats = [CSV]
    actions_detail = ["process_wallet_transaction"]

    @action(
        description=_("Process Transaction"),
        url_path="process-transaction",
        permissions=["change", "can_change_money"],
        icon="add_card",
        variant=ActionVariant.PRIMARY,
    )
    def process_wallet_transaction(self, request: HttpRequest, object_id: int):
        wallet = get_object_or_404(Wallet, pk=object_id)
        form = WalletTransactionForm(request.POST or None, request.FILES or None)

        if request.method == "POST" and form.is_valid():
            WalletTransactionService.create_transaction(
                wallet=wallet,
                amount=Money(form.cleaned_data["amount"], wallet.balance.currency),
                transaction_type=form.cleaned_data["transaction_type"],
                action_by=request.user,
                transaction_note=form.cleaned_data["note"],
                attachment=form.cleaned_data["attachment"],
            )
            return redirect(
                reverse_lazy("admin:payment_wallet_change", args=[object_id])
            )
        context = {
            "form": form,
            "phone_number": wallet.user.phone_number,
            "email": wallet.user.email,
            "balance": wallet.balance,
            "title": _("Process Transaction"),
            **self.admin_site.each_context(request),
        }
        return render(request, "admin/wallet/process_transaction_form.html", context)

    def has_can_change_money_permission(self, request: HttpRequest, obj=None):
        user = request.user
        return isinstance(user, AdminUser) and user.can_access_money
