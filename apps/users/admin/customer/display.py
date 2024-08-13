from unfold.decorators import display

from apps.users.models.customer import Customer


class CustomerDisplayMixin:
    @display(description="Provider", header=True, ordering="phone_number")
    def display_header(self, customer: Customer):
        return [
            customer,
            customer.full_name,
            "CU",
            {
                "path": customer.image.url if customer.image else None,
            },
        ]

    @display(
        description="Is Active?",
        label={"True": "success", "False": "danger"},
        ordering="-is_active",
    )
    def display_is_active(self, customer: Customer):
        return "True" if customer.is_active else "False"

    @display(
        description="Is Verified?",
        label={"True": "success", "False": "danger"},
        ordering="-is_phone_verified",
    )
    def display_is_phone_verified(self, customer: Customer):
        return "True" if customer.is_phone_verified else "False"
