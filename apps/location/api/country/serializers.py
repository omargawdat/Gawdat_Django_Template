from rest_framework.serializers import ModelSerializer

from apps.location.models.country import Country


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "code",
            "name",
            "flag",
            "phone_code",
            "phone_example",
            "max_phone_length",
            "currency",
            "currency_symbol",
            "alpha_3",
        ]
