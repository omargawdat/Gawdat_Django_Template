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
    def get_customer_by_phone(*, phone_number):
        try:
            return Customer.objects.get(user__phone_number=phone_number)
        except Customer.DoesNotExist:
            return None

    @staticmethod
    def is_email_exists(email: str) -> bool:
        return Customer.objects.filter(user__email=email).exists()
