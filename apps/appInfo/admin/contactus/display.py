from typing import TYPE_CHECKING

from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.appInfo.models.contact_us import ContactUs
from apps.appInfo.other.constants import ContactCategory

if TYPE_CHECKING:
    from apps.users.models.customer import Customer


class ContactUsDisplayMixin:
    @display(description="Customer", header=True)
    def display_header(self, contact_us: ContactUs):
        """Display header with image if available."""
        customer: Customer = contact_us.customer
        display_name = "Anonymous"
        if customer:
            display_name = customer.full_name or customer.email
        return [
            display_name,
            f"{customer.phone_number if customer else ''}",
            f"#{contact_us.pk}",
            "",
        ]

    @display(description="Description")
    def display_description(self, contact_us: ContactUs):
        return f"{contact_us.description[:80]}..."

    @display(
        description=_("Contact Type"),
        label={
            ContactCategory.GENERAL.label: "success",
            ContactCategory.SUPPORT.label: "info",
            ContactCategory.FEEDBACK.label: "warning",
            ContactCategory.OTHER.label: "secondary",
            ContactCategory.COMPLAINT.label: "danger",
        },
    )
    def display_contact_type(self, contact_us: ContactUs):
        return contact_us.get_contact_type_display()

    @display(description="Created Ago", label="info", ordering="created_at")
    def display_created_at(self, contact_us: ContactUs):
        return f"{timesince(contact_us.created_at, timezone.now())}"
