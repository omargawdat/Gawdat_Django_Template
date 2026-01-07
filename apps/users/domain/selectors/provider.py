from datetime import timedelta

from django.utils import timezone

from apps.users.models.provider import Provider


class ProviderSelector:
    @staticmethod
    def last_week_new_provider_count():
        return Provider.objects.filter(
            user__date_joined__gte=timezone.now() - timedelta(days=7)
        ).count()

    @staticmethod
    def is_email_exists(email: str) -> bool:
        return Provider.objects.filter(user__email=email).exists()

    # ========================================
    # Insight Selectors (Static values for now)
    # ========================================

    @staticmethod
    def get_avg_orders_per_provider() -> float:
        """Get average orders per provider. Static value for now."""
        return 8.2

    @staticmethod
    def get_avg_revenue_per_provider() -> str:
        """Get average revenue per provider. Static value for now."""
        return "2,450.00 SAR"

    @staticmethod
    def get_providers_joined_today() -> int:
        """Get number of providers who joined today. Static value for now."""
        return 3

    @staticmethod
    def get_top_rated_providers_percentage() -> str:
        """Get percentage of providers with rating > 4.5. Static value for now."""
        return "62%"
