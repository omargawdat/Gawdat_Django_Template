from rest_framework import serializers

from apps.location.models.region import Region


class RegionMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["code", "name", "country"]
