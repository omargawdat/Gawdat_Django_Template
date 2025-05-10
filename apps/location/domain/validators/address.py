from rest_framework.exceptions import ValidationError

from apps.location.domain.selector.address import AddressSelector
from apps.location.errors import LocationError
from apps.location.models.address import Address
from apps.users.models.customer import Customer


class AddressValidator:
    @staticmethod
    def validate_not_primary_address(*, address: Address, customer: Customer) -> None:
        if AddressSelector.is_primary_address(address=address, customer=customer):
            raise ValidationError(
                LocationError.CANNOT_DELETE_PRIMARY_ADDRESS.message,
                code=LocationError.CANNOT_DELETE_PRIMARY_ADDRESS.code,
            )
