from rest_framework.response import Response
from rest_framework.views import APIView

from apps.location.api.region.serializers import PointSerializer
from apps.location.domain.selector.region import RegionSelector


class RegionByPointView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PointSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        point = serializer.validated_data["point"]

        region_code = RegionSelector.get_region_code_by_point(point=point)

        return Response({"region_code": region_code})
