from django.utils import timezone
from django.utils.html import format_html
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

    @display(description=_("Created ago"), label="info")
    def display_created_at_time(self, payment: Payment):
        return f"{timesince(payment.created_at, timezone.now())}"

    @display(description=_("Price"), ordering="price_after_discount")
    def display_price(self, payment: Payment):
        discount_amount = payment.price_before_discount - payment.price_after_discount
        if discount_amount.amount > 0:
            discount_percent = int(
                (discount_amount.amount / payment.price_before_discount.amount) * 100
            )
            return format_html(
                '<del style="color: #888;">{}</del> → <strong>{}</strong> '
                '<span style="color: #16a34a;">(-{}%)</span>',
                payment.price_before_discount,
                payment.price_after_discount,
                discount_percent,
            )
        return format_html(
            "<strong>{}</strong>",
            payment.price_before_discount,
        )
