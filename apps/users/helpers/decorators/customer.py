from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.users.models.customer import Customer


class CustomerDisplayMixin:
    @display(description=_("Customer"), header=True)
    def display_header(self, customer: Customer):
        return [
            customer,
            None,
            "CU",
            {
                "path": customer.image.url if customer.image else None,
            },
        ]

    @display(description=_("Phone Number"), label=True)
    def display_phone_number(self, customer: Customer):
        return customer.phone_number
