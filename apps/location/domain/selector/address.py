from django.db.models import Case
from django.db.models import IntegerField
from django.db.models import QuerySet
from django.db.models import Value
from django.db.models import When

from apps.location.models.address import Address
from apps.users.models.customer import Customer


class AddressSelector:
    @staticmethod
    def get_all_customer_addresses(*, customer: Customer) -> QuerySet[Address]:
        addresses = Address.objects.filter(customer=customer)
        if customer.primary_address:
            addresses = addresses.annotate(
                is_primary=Case(
                    When(id=customer.primary_address.id, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ).order_by("-is_primary")
        return addresses

    @staticmethod
    def is_customer_address(address: Address, customer: Customer) -> bool:
        return address.customer == customer

    @staticmethod
    def is_primary_address(*, address: Address, customer: Customer) -> bool:
        return customer.primary_address_id == address.id
