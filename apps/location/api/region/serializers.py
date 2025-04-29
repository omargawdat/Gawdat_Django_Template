from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField


class PointSerializer(serializers.Serializer):
    point = GeometryField()
