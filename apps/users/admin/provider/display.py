from unfold.decorators import display

from apps.users.models.provider import Provider


class ProviderDisplayMixin:
    @display(description="Provider", header=True, ordering="phone_number")
    def display_header(self, provider: Provider):
        return [
            provider.phone_number,
            provider.full_name,
            "CU",
            {
                "path": provider.image.url if provider.image else None,
            },
        ]

    @display(
        description="Is Active?",
        label={"True": "success", "False": "danger"},
        ordering="-is_active",
    )
    def display_is_active(self, provider: Provider):
        return "True" if provider.is_active else "False"

    @display(
        description="Is Verified?",
        label={"True": "success", "False": "danger"},
        ordering="-is_phone_verified",
    )
    def display_is_phone_verified(self, provider: Provider):
        return "True" if provider.is_phone_verified else "False"
