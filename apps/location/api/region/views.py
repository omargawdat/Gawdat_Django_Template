from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.location.domain.selector.region import RegionSelector


class RegionByPointView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            longitude = float(request.query_params.get("long"))
            latitude = float(request.query_params.get("lat"))
        except (TypeError, ValueError):
            return Response(
                {"detail": "Missing or invalid 'long' or 'lat' query parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        point = Point(longitude, latitude, srid=4326)
        region_code = RegionSelector.get_region_code_by_point(point=point)
        return Response({"region_code": region_code})
