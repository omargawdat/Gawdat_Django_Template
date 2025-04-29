from unfold.decorators import display

from apps.products.models.brand import Brand


class BrandDisplayMixin:
    @display(description="brand", header=True)
    def display_header(self, brand: Brand):
        """Display header with image if available."""
        return [
            brand.name,
            "",
            "O",
            {"path": brand.logo.url if hasattr(brand, "logo") and brand.logo else None},
        ]
