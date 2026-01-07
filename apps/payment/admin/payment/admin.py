from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import XLSX
from unfold.contrib.import_export.forms import ExportForm

from apps.payment.domain.selectors.payment import PaymentSelector
from apps.payment.models.payment import Payment
from common.base.admin import BaseModelAdmin

from .change_view import PaymentChangeView
from .display import PaymentDisplayMixin
from .list_view import PaymentListView
from .permissions import PaymentAdminPermissions
from .resource import PaymentResource


@admin.register(Payment)
class PaymentAdmin(
    PaymentDisplayMixin,
    PaymentListView,
    PaymentChangeView,
    PaymentAdminPermissions,
    ExportActionModelAdmin,
    BaseModelAdmin,
):
    resource_class = PaymentResource
    export_form_class = ExportForm
    formats = [XLSX]
    change_list_template = "admin/payment/payment/change_list.html"
    import_export_change_list_template = "admin/payment/payment/change_list.html"

    def changelist_view(self, request, extra_context=None):
        payments_today = PaymentSelector.get_payments_today()
        success_rate = PaymentSelector.get_success_rate()
        wallet_usage = PaymentSelector.get_wallet_usage()
        total_revenue_today = PaymentSelector.get_total_revenue_today()

        cards = [
            {
                "title": _("Payments Today"),
                "value": payments_today,
                "description": _("Number of payments processed today"),
            },
            {
                "title": _("Success Rate"),
                "value": success_rate,
                "description": _("Percentage of successful payments"),
            },
            {
                "title": _("Wallet Usage"),
                "value": wallet_usage,
                "description": _("Percentage of payments using wallet"),
            },
            {
                "title": _("Revenue Today"),
                "value": total_revenue_today,
                "description": _("Total revenue from paid payments today"),
            },
        ]

        extra_context = extra_context or {}
        extra_context.update({"payment_cards": cards})
        return super().changelist_view(request, extra_context=extra_context)
