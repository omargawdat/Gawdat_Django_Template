from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.payment.constants import PaymentType
from apps.payment.models.payment import Payment


class PaymentDisplayMixin:
    @display(description="Payment Info", header=True)
    def display_header(self, payment: Payment):
        """Display header with image if available."""
        return [
            f"Payment: {payment.pk}",
            f"Customer: {payment.customer.email or payment.customer.full_name}",
        ]

    @display(
        description=_("Payment Method"),
        label={
            PaymentType.charge_wallet.label: "info",
            PaymentType.other.label: "warning",
        },
    )
    def display_payment_type(self, payment: Payment):
        return payment.get_payment_type_display()

    @display(
        description=_("Payment Price"), label="info", ordering=("price_after_discount")
    )
    def display_payment_price(self, payment: Payment):
        return payment.price_after_discount

    @display(description=_("Created ago"), label="info")
    def display_created_at_time(self, payment: Payment):
        return f"{timesince(payment.created_at, timezone.now())}"
