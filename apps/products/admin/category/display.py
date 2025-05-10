from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.products.models.category import Category


class CategoryDisplayMixin:
    @display(description="Category ID", header=True)
    def display_header(self, category: Category):
        """Display header with image if available."""
        return [
            category.pk,
            "",
            "O",
            {
                "path": category.image.url
                if hasattr(category, "image") and category.image
                else None
            },
        ]

    @display(description=_("Total Products"), label="info")
    def display_products_count(self, category: Category):
        return category.products.count()
