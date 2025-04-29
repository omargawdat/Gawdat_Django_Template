from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.api.banner.serializers import BannerListSerializer
from apps.products.api.brand.serializers import BrandListSerializer
from apps.products.api.category.serializers import CategoryListSerializer
from apps.products.api.product.serializers import ProductListSerializer
from apps.products.domain.selectors.banner import BannerSelector
from apps.products.domain.selectors.brand import BrandSelector
from apps.products.domain.selectors.category import CategorySelector
from apps.products.domain.selectors.product import ProductSelector


class HomeListView(APIView):
    permission_classes = []

    def get(self, request):
        serialized_categories = CategoryListSerializer(
            CategorySelector.get_categories(), many=True, context={"request": request}
        ).data
        serialized_brands = BrandListSerializer(
            BrandSelector.get_brands(), many=True, context={"request": request}
        ).data
        serialized_banners = BannerListSerializer(
            BannerSelector.get_banners(), many=True, context={"request": request}
        ).data
        serialized_products = ProductListSerializer(
            ProductSelector.get_products(), many=True, context={"request": request}
        ).data

        response_data = {
            "banners": serialized_banners,
            "categories": serialized_categories,
            "recommended_products": serialized_products,
            "bought_products": serialized_products,
            "brands": serialized_brands,
        }

        return Response(response_data)
