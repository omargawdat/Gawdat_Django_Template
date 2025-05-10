from rest_framework import generics

from apps.products.domain.selectors.product import ProductSelector

from .serializers import ProductListSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = []

    def get_queryset(self):
        category_id = self.request.query_params.get("category")
        return ProductSelector.get_products_by_category(category_id=category_id)
