from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.location.domain.selector.address import AddressSelector
from apps.location.models.address import Address
from apps.users.models.customer import Customer


class CustomerValidator:
    @staticmethod
    def validate_address_belongs_to_customer(
        *, address: Address, customer: Customer
    ) -> None:
        if address and not AddressSelector.is_customer_address(address, customer):
            raise ValidationError(_("The address must belong to the customer."))

    @staticmethod
    def authenticate(email: str, password: str) -> Customer:
        email = email.strip().lower()
        customer = Customer.objects.filter(user__email__iexact=email).first()

        if not customer or not customer.check_password(password):
            raise ValueError("Invalid email or password.")

        if not customer.is_active:
            raise ValueError("Account is disabled.")

        return customer
