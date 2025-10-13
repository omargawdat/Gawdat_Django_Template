from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from unfold.decorators import action

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
    BaseModelAdmin,
):
    actions_detail = ["view_wallet"]

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
