from rest_framework import serializers

from apps.products.models.banner import Banner


class BannerMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = (
            "pk",
            "image",
            "banner_type",
        )


class BannerListSerializer(BannerMinimalSerializer):
    class Meta(BannerMinimalSerializer.Meta):
        fields = [
            *BannerMinimalSerializer.Meta.fields,
        ]
