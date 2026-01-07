from django.contrib.admin.utils import display_for_field
from django.contrib.admin.utils import label_for_field
from django.contrib.admin.utils import lookup_field
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.sections import TableSection

from apps.payment.models.wallet_transaction import WalletTransaction


class ProviderWalletTransactionSection(TableSection):
    verbose_name = _("The Latest 7 Wallet Transactions")
    height = 300
    fields = [
        "id",
        "transaction_type",
        "amount",
        "created_at",
        "view_detail",
    ]

    def transaction_type(self, instance):
        """Display transaction type with color."""
        credit_types = [
            "REFUND",
            "CHARGING",
            "CANCEL_ORDER",
            "SHARE",
            "CASH_RECEIVE",
            "REFERRAL",
            "REFERRAL_APP_INSTALL_INVITER",
            "REFERRAL_APP_INSTALL_INVITEE",
            "REFERRAL_ORDER_INVITER",
            "REFERRAL_ORDER_INVITEE",
        ]
        color = "green" if instance.transaction_type in credit_types else "red"
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            instance.get_transaction_type_display(),
        )

    transaction_type.short_description = _("Type")

    def created_at(self, instance):
        """Format created_at datetime."""
        return instance.created_at.strftime("%Y-%m-%d %H:%M")

    created_at.short_description = _("Created At")

    def view_detail(self, instance):
        """Link to wallet transaction detail."""
        url = reverse("admin:payment_wallettransaction_change", args=[instance.pk])
        return format_html('<a href="{}">👁</a>', url)

    view_detail.short_description = _("Detail")

    def get_queryset(self):
        """Get wallet transactions through user.wallet.transactions."""
        try:
            wallet = self.instance.user.wallet
            return wallet.transactions.order_by("-created_at")[:7]
        except Exception:
            return WalletTransaction.objects.none()

    def render(self) -> str:
        headers = []
        rows = []

        # Get transactions via the indirect relationship
        filtered_results = self.get_queryset()

        for field_name in self.fields:
            if hasattr(self, field_name):
                if hasattr(getattr(self, field_name), "short_description"):
                    headers.append(getattr(self, field_name).short_description)
                else:
                    headers.append(field_name)
            else:
                headers.append(label_for_field(field_name, WalletTransaction))

        for result in filtered_results:
            row = []
            for field_name in self.fields:
                if hasattr(self, field_name):
                    row.append(getattr(self, field_name)(result))
                else:
                    field, _attr, value = lookup_field(field_name, result)
                    row.append(display_for_field(value, field, "-"))
            rows.append(row)

        context = {
            "request": self.request,
            "table": {
                "headers": headers,
                "rows": rows,
            },
        }

        if hasattr(self, "verbose_name") and self.verbose_name:
            context["title"] = self.verbose_name

        if hasattr(self, "height") and self.height:
            context["height"] = self.height

        return render_to_string(
            "unfold/components/table.html",
            context=context,
        )
