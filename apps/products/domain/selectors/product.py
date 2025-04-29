from django.db.models import QuerySet

from apps.products.models.product import Product


class ProductSelector:
    @staticmethod
    def get_products() -> QuerySet[Product]:
        return Product.objects.all()

    @staticmethod
    def get_products_by_category(
        *, category_id: int | None = None
    ) -> QuerySet[Product]:
        queryset = Product.objects.all()
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
