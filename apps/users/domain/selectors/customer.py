from datetime import timedelta

from django.utils import timezone

from apps.users.models.customer import Customer


class CustomerSelector:
    @staticmethod
    def last_week_new_customer_count():
        return Customer.objects.filter(
            user__date_joined__gte=timezone.now() - timedelta(days=7)
        ).count()

    @staticmethod
    def is_profile_completed(customer: Customer) -> bool:
        required_fields = [
            customer.full_name,
            customer.email,
            customer.gender,
            customer.birth_date,
        ]
        return all(required_fields)

    @staticmethod
    def is_email_exists(email: str) -> bool:
        return Customer.objects.filter(user__email=email).exists()

    # ========================================
    # Insight Selectors (Static values for now)
    # ========================================

    @staticmethod
    def get_avg_orders_per_customer() -> float:
        """Get average sessions per customer. Static value for now."""
        return round(3.5)

    @staticmethod
    def get_avg_payment_per_customer() -> str:
        """Get average payment amount per customer. Static value for now."""
        return "150.00 SAR"

    @staticmethod
    def get_customers_joined_today() -> int:
        """Get number of customers who joined today. Static value for now."""
        return 12

    @staticmethod
    def get_repeat_customers_percentage() -> str:
        """Get percentage of customers with more than 2 paid payments. Static value for now."""
        return "45%"
