from apps.appInfo.models.social import SocialAccount
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
        return {"value": 200, "currency": "SAR", "display": "200 SAR"}

    @staticmethod
    def get_social_accounts():
        return SocialAccount.get_solo()
