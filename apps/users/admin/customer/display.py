from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.users.models.customer import Customer


class CustomerDisplayMixin:
    @display(description=_("Customer"), header=True)
    def display_customer_info(self, customer: Customer):
        return [
            customer.full_name or customer.email,
            _("Email: %s") % customer.email,
            "CO",
            {
                "path": customer.image.url if customer.image else None,
                "squared": False,
                "borderless": True,
            },
        ]

    @display(
        label={"True": "success", "False": "danger"},
        description=_("Is Active"),
        ordering="user__is_active",
    )
    def display_is_active_customer(self, customer: Customer) -> str:
        return _("True") if customer.is_active else _("False")

    @display(description=_("Date joined ago"), label="info")
    def display_date_joined_time(self, customer: Customer):
        return f"{timesince(customer.date_joined, timezone.now())}"
