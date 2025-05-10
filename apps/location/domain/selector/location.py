from django.contrib.gis.geos import Point

from apps.location.domain.selector.region import RegionSelector
from apps.location.models.country import Country
from apps.location.models.region import Region
from apps.users.models.customer import Customer


class LocationSelector:
    @staticmethod
    def get_country_by_point(point: Point) -> Country | None:
        region = RegionSelector.get_region_by_point(point=point)
        return Country.objects.get(code=region.country) if region else None

    @staticmethod
    def is_region_country_match_user(region: Region, user: Customer) -> bool:
        return region.country_id == user.country_id
