from drf_spectacular.utils import extend_schema
from rest_framework import generics

from apps.location.api.country.serializers import CountryDetailedSerializer
from apps.location.domain.selector.country import CountrySelector


@extend_schema(
    tags=["Location/Country"],
    operation_id="ListCountries",
)
class ActiveCountryList(generics.ListAPIView):
    serializer_class = CountryDetailedSerializer
    queryset = CountrySelector.get_active_countries()
    permission_classes = []
