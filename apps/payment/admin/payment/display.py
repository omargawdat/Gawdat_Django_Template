from unfold.decorators import display

from apps.payment.models.payment import Payment


class PaymentDisplayMixin:
    @display(description="Payment ID", header=True)
    def display_header(self, payment: Payment):
        """Display header with image if available."""
        return [
            payment.pk,
            "",
            "O",
        ]
