from unfold.decorators import display

from apps.products.models.product import Product


class ProductDisplayMixin:
    @display(description="Product Info", header=True)
    def display_header(self, product: Product):
        """Display header with image if available."""
        return [
            f"Product ID: {product.pk}",
            f"Product Name: {product.name}",
            "O",
            {
                "path": product.image.url
                if hasattr(product, "image") and product.image
                else None
            },
        ]
