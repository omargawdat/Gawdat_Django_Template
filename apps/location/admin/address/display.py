from unfold.decorators import display

from apps.location.models.address import Address


class AddressDisplayMixin:
    @display(description="address", header=True)
    def display_header(self, address: Address):
        """Display header with image if available."""
        return [
            address.pk,
            "",
            "O",
            {
                "path": address.image.url
                if hasattr(address, "image") and address.image
                else None
            },
        ]
