from apps.location.domain.selector.country import CountrySelector
from apps.users.domain.validators.user import UserValidator
from apps.users.models.customer import Customer


class CustomerService:
    @staticmethod
    def get_or_create_active_customer(phone_number: str) -> tuple[Customer, bool]:
        customer, created = Customer.objects.get_or_create(phone_number=phone_number)
        UserValidator.validate_user_is_active(customer)
        return customer, created

    @staticmethod
    def update_or_create_customer(
        *, phone_number: str, language: str
    ) -> tuple[Customer, bool]:
        defaults = {
            "username": str(phone_number),
            "language": language,
            "country": CountrySelector.country_by_phone(phone_number),
        }

        customer, created = Customer.objects.update_or_create(
            phone_number=phone_number, defaults=defaults
        )

        customer.clean()
        customer.save()

        return customer, created
