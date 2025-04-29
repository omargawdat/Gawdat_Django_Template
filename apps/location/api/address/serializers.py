from rest_framework import serializers
from rest_framework_gis import fields as gis_fields

from apps.location.models.address import Address


class AddressMinimalSerializer(serializers.ModelSerializer):
    point = gis_fields.GeometryField()

    class Meta:
        model = Address
        fields = ["id", "description", "location_type", "point"]


class AddressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = AddressMinimalSerializer.Meta.fields


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "point", "description", "location_type"]


class AddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["point", "description", "location_type"]
