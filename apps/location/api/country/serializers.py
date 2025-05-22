from rest_framework.serializers import ModelSerializer

from apps.location.models.country import Country


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ["code", "flag", "phone_code", "name"]
