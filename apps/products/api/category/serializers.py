from rest_framework import serializers

from apps.products.models.category import Category


class CategoryMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "pk",
            "name",
            "image",
        )


class CategoryListSerializer(CategoryMinimalSerializer):
    class Meta(CategoryMinimalSerializer.Meta):
        fields = [
            *CategoryMinimalSerializer.Meta.fields,
        ]
