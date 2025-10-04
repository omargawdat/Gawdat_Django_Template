from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.location.api.country.serializers import CountrySerializer
from apps.location.domain.selector.country import CountrySelector


class ActiveCountryList(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["Location/Country"],
        operation_id="ListCountries",
        responses={200: CountrySerializer(many=True)},
    )
    def get(self, request):
        queryset = CountrySelector.get_active_countries()
        serializer = CountrySerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)
