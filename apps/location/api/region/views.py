from django.contrib.gis.geos import Point
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.location.api.region.serializers import RegionMinimalSerializer
from apps.location.domain.selector.region import RegionSelector


class RegionByPointView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["Location/Region"],
        operation_id="GetRegionByPoint",
        description="""
        - Cairo, Egypt: `?long=31.235712&lat=30.044420`
        - Riyadh, Saudi Arabia: `?long=46.738586&lat=24.774265`
        """,
        parameters=[
            OpenApiParameter(
                name="long",
                type=OpenApiTypes.FLOAT,
                required=True,
                examples=[
                    OpenApiExample(
                        "Saudi Arabia Example",
                        value=46.738586,
                    ),
                ],
            ),
            OpenApiParameter(
                name="lat",
                type=OpenApiTypes.FLOAT,
                required=True,
                examples=[
                    OpenApiExample(
                        "Saudi Arabia Example",
                        value=24.774265,
                    ),
                ],
            ),
        ],
        responses={
            200: RegionMinimalSerializer,
        },
    )
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
        region = RegionSelector.get_region_by_point(point=point)
        serialized_region = RegionMinimalSerializer(region)
        return Response(serialized_region.data, status=status.HTTP_200_OK)
