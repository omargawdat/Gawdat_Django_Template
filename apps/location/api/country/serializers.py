from rest_framework.serializers import ModelSerializer

from apps.location.models.country import Country


class CountryMinimalSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ["code", "flag", "phone_code", "name"]


class CountryDetailedSerializer(CountryMinimalSerializer):
    class Meta(CountryMinimalSerializer.Meta):
        fields = CountryMinimalSerializer.Meta.fields
