from apps.location.models.address import Address
from apps.users.models.customer import Customer


class AddressSelector:
    @staticmethod
    def get_all_customer_addresses(*, customer: Customer) -> list[Address]:
        return Address.objects.filter(customer=customer)

    @staticmethod
    def is_customer_address(address: Address, customer: Customer) -> bool:
        return address.customer == customer
