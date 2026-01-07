from django.db.models import Sum
from django.utils import timezone

from apps.payment.constants import PaymentType
from apps.payment.models.payment import Payment


class PaymentSelector:
    @staticmethod
    def get_payments_today() -> int:
        """Get count of payments created today."""
        today = timezone.now().date()
        return Payment.objects.filter(created_at__date=today).count()

    @staticmethod
    def get_success_rate() -> str:
        """Get percentage of payments that are paid."""
        total = Payment.objects.count()
        if total == 0:
            return "0%"
        paid = Payment.objects.filter(is_paid=True).count()
        rate = (paid / total) * 100
        return f"{rate:.0f}%"

    @staticmethod
    def get_wallet_usage() -> str:
        """Get percentage of payments using wallet."""
        total = Payment.objects.count()
        if total == 0:
            return "0%"
        wallet_payments = Payment.objects.filter(
            payment_type=PaymentType.charge_wallet
        ).count()
        rate = (wallet_payments / total) * 100
        return f"{rate:.0f}%"

    @staticmethod
    def get_total_revenue_today() -> str:
        """Get total revenue from paid payments today."""
        today = timezone.now().date()
        result = Payment.objects.filter(
            created_at__date=today,
            is_paid=True,
        ).aggregate(total=Sum("price_after_discount"))
        total = result["total"] or 0
        return f"{total:,.2f} SAR"
