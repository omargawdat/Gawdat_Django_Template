from rest_framework import serializers
from rest_framework_gis import fields as gis_fields

from apps.location.models.address import Address


class AddressMinimalSerializer(serializers.ModelSerializer):
    point = gis_fields.GeometryField()

    class Meta:
        model = Address
        fields = [
            "id",
            "description",
            "location_type",
            "point",
            "map_description",
            "map_image",
        ]


class AddressDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = AddressMinimalSerializer.Meta.fields


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
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
            "point",
            "description",
            "map_description",
            "location_type",
            "map_image",
        ]
