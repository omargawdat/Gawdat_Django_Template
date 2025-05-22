from django.contrib.gis.geos import Point

from apps.location.api.exceptions import RegionCountryMismatchException
from apps.location.api.exceptions import UnsupportedRegionException
from apps.location.domain.selector.location import LocationSelector
from apps.location.domain.selector.region import RegionSelector
from apps.location.models.region import Region
from apps.users.models import User


class RegionValidator:
    @staticmethod
    def validate_point_inside_a_region(*, point: Point) -> None:
        region = RegionSelector.get_region_by_point(point=point)
        if not region:
            raise UnsupportedRegionException

    @staticmethod
    def validate_user_country_match(*, region: Region, user: User) -> None:
        if not LocationSelector.is_region_country_match_user(region, user):
            raise RegionCountryMismatchException

    @staticmethod
    def validate_user_location(*, point: Point, user: User) -> None:
        region = RegionSelector.get_region_by_point(point=point)

        RegionValidator.validate_point_inside_a_region(point=point)
        RegionValidator.validate_user_country_match(region=region, user=user)
