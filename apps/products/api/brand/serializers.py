from rest_framework import serializers

from apps.products.models.brand import Brand


class BrandMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "pk",
            "name",
            "logo",
        )


class BrandListSerializer(BrandMinimalSerializer):
    class Meta(BrandMinimalSerializer.Meta):
        fields = [
            *BrandMinimalSerializer.Meta.fields,
        ]
