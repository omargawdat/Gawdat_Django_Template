from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import XLSX
from simple_history.admin import SimpleHistoryAdmin
from unfold.contrib.import_export.forms import ExportForm
from unfold.decorators import action

from apps.users.admin.customer.resource import CustomerResource
from apps.users.domain.selectors.customer import CustomerSelector
from apps.users.models.customer import Customer
from common.base.admin import BaseModelAdmin

from .change_view import CustomerChangeView
from .display import CustomerDisplayMixin
from .list_view import CustomerListView
from .permissions import CustomerAdminPermissions


@admin.register(Customer)
class CustomerAdmin(
    CustomerDisplayMixin,
    CustomerListView,
    CustomerChangeView,
    CustomerAdminPermissions,
    ExportActionModelAdmin,
    SimpleHistoryAdmin,
    BaseModelAdmin,
):
    resource_class = CustomerResource
    export_form_class = ExportForm
    formats = [XLSX]
    actions_detail = ["view_wallet"]
    change_list_template = "admin/users/customer/change_list.html"
    import_export_change_list_template = "admin/users/customer/change_list.html"

    @action(
        description=_("View Customer Wallet"),
        url_path="view-wallet",
        attrs={"class": "addlink"},
    )
    def view_wallet(self, request: HttpRequest, object_id: int):
        """Redirect to the customer's wallet in the Wallet admin."""
        customer = Customer.objects.select_related("user").get(pk=object_id)

        # Check if customer has a wallet
        if hasattr(customer.user, "wallet"):
            wallet_id = customer.user.wallet.pk
            return redirect(
                reverse_lazy("admin:payment_wallet_change", args=(wallet_id,))
            )

        # If no wallet exists, redirect back with a message
        self.message_user(
            request, _("This customer does not have a wallet yet."), level="warning"
        )
        return redirect(reverse_lazy("admin:users_customer_change", args=(object_id,)))

    def has_view_wallet_permission(
        self, request: HttpRequest, object_id: str | int
    ) -> bool:
        """Check if user has permission to view the wallet."""
        # Allow if user can view wallets
        return request.user.has_perm("payment.view_wallet")

    def changelist_view(self, request, extra_context=None):
        avg_orders = CustomerSelector.get_avg_orders_per_customer()
        avg_payment = CustomerSelector.get_avg_payment_per_customer()
        total_customers_per_day = CustomerSelector.get_customers_joined_today()
        repeat_customer_rate = CustomerSelector.get_repeat_customers_percentage()

        cards = [
            {
                "title": _("Avg Order Per Client"),
                "value": avg_orders,
                "description": _("Average number of orders per customer"),
            },
            {
                "title": _("Avg Payment Per Client"),
                "value": avg_payment,
                "description": _("Average total amount paid by each client"),
            },
            {
                "title": _("Clients Joined Today"),
                "value": total_customers_per_day,
                "description": _("Number of new clients who signed up today"),
            },
            {
                "title": _("Repeat Customers"),
                "value": repeat_customer_rate,
                "description": _(
                    "Percentage of clients who has more than 2 paid payment"
                ),
            },
        ]

        extra_context = extra_context or {}
        extra_context.update(
            {
                "customer_cards": cards,
            }
        )
        return super().changelist_view(request, extra_context=extra_context)
