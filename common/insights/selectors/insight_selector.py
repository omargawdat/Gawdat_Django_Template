import calendar

from django.db.models import Count
from django.db.models import Sum
from django.db.models.functions import Extract
from django.utils import timezone

from apps.appInfo.models.contact_us import ContactUs
from apps.appInfo.models.social import SocialAccount
from apps.payment.models.payment import Payment
from apps.users.models.customer import Customer


class InsightSelector:
    @staticmethod
    def get_total_active_customer() -> int:
        return Customer.objects.filter(is_active=True, is_verified=True).count()

    @staticmethod
    def get_total_paid_orders() -> int:
        return 100

    @staticmethod
    def get_total_revenue() -> dict:
        payments = Payment.objects.filter(is_paid=True)

        # Handle case where there are no payments
        if not payments.exists():
            return {
                "value": 0.0,
                "currency": "SAR",  # Default currency
                "display": "0.00 SAR",
            }

        # Get currency from first payment
        first_payment = payments.first()
        currency = first_payment.price_after_discount.currency

        # Sum the decimal amounts
        total_amount = payments.aggregate(total=Sum("price_after_discount"))["total"]

        # Handle case where total_amount is None (shouldn't happen but be safe)
        if total_amount is None:
            total_amount_value = 0.0
            display_amount = f"0.00 {currency}"
        else:
            total_amount_value = float(total_amount)
            display_amount = f"{total_amount} {currency}"

        return {
            "value": total_amount_value,
            "currency": str(currency),
            "display": display_amount,
        }

    @staticmethod
    def get_unchecked_contacts(limit: int = 10) -> list[ContactUs]:
        return ContactUs.objects.filter(has_checked=False)

    @staticmethod
    def get_social_accounts() -> SocialAccount:
        return SocialAccount.get_solo()

    @staticmethod
    def get_monthly_payment_data() -> dict:
        """Get daily payment data for current month"""

        # Get current month payments
        current_date = timezone.now()
        current_month_payments = Payment.objects.filter(
            is_paid=True,
            created_at__year=current_date.year,
            created_at__month=current_date.month,
        )

        # Group by day and sum amounts
        daily_data = (
            current_month_payments.annotate(day=Extract("created_at", "day"))
            .values("day")
            .annotate(total=Sum("price_after_discount"), count=Count("id"))
            .order_by("day")
        )

        # Create arrays for all days of the month
        days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
        labels = [str(i) for i in range(1, days_in_month + 1)]
        amounts = [0] * days_in_month
        counts = [0] * days_in_month

        # Fill in actual data
        for item in daily_data:
            day_index = item["day"] - 1
            amounts[day_index] = float(item["total"]) if item["total"] else 0
            counts[day_index] = item["count"]

        return {"labels": labels, "amounts": amounts, "counts": counts}

    @staticmethod
    def get_yearly_payment_data() -> dict:
        """Get monthly payment data for current year"""

        current_date = timezone.now()
        current_year_payments = Payment.objects.filter(
            is_paid=True, created_at__year=current_date.year
        )

        # Group by month and sum amounts
        monthly_data = (
            current_year_payments.annotate(month=Extract("created_at", "month"))
            .values("month")
            .annotate(total=Sum("price_after_discount"), count=Count("id"))
            .order_by("month")
        )

        # Create arrays for all months
        month_labels = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        amounts = [0] * 12
        counts = [0] * 12

        # Fill in actual data
        for item in monthly_data:
            month_index = item["month"] - 1
            amounts[month_index] = float(item["total"]) if item["total"] else 0
            counts[month_index] = item["count"]

        return {"labels": month_labels, "amounts": amounts, "counts": counts}
