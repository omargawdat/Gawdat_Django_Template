from rest_framework import serializers
from rest_framework_gis import fields as gis_fields

from apps.location.models.address import Address


class AddressMinimalSerializer(serializers.ModelSerializer):
    point = gis_fields.GeometryField()
    is_primary = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = [
            "id",
            "country",
            "description",
            "location_type",
            "point",
            "map_description",
            "map_image",
            "is_primary",
        ]

    def get_is_primary(self, obj) -> bool:
        """Check if this address is the customer's primary address"""
        return obj.customer.primary_address_id == obj.id


class AddressDetailedSerializer(AddressMinimalSerializer):
    class Meta(AddressMinimalSerializer.Meta):
        pass


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "country",
            "point",
            "description",
            "map_description",
            "location_type",
            "map_image",
        ]


class AddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "country",
            "point",
            "description",
            "map_description",
            "location_type",
            "map_image",
        ]
