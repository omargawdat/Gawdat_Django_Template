from rest_framework import serializers

from apps.products.models.product import Product


class ProductMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "description",
            "price",
            "price_currency",
            "image",
        )


class ProductListSerializer(ProductMinimalSerializer):
    class Meta(ProductMinimalSerializer.Meta):
        fields = [
            *ProductMinimalSerializer.Meta.fields,
            "category",
        ]
