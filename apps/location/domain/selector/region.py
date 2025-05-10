from django.contrib.gis.geos import Point

from apps.location.models.region import Region


class RegionSelector:
    @staticmethod
    def get_region_by_point(*, point: Point) -> Region | None:
        try:
            return Region.objects.get(geometry__contains=point)
        except Region.DoesNotExist:
            return None

    @staticmethod
    def get_region_code_by_point(*, point: Point) -> str | None:
        region = RegionSelector.get_region_by_point(point=point)
        return region.pk if region else None
