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
