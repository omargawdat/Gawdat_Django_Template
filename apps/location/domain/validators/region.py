from constance import config
from django.contrib.gis.geos import Point

from apps.location.api.exceptions import InactiveCountryException
from apps.location.api.exceptions import RegionCountryMismatchException
from apps.location.api.exceptions import UnsupportedRegionException
from apps.location.domain.selector.location import LocationSelector
from apps.location.domain.selector.region import RegionSelector
from apps.location.models.country import Country
from apps.location.models.region import Region
from apps.users.models import User


class RegionValidator:
    @staticmethod
    def validate_point_inside_a_region(*, point: Point) -> Region:
        region = RegionSelector.get_region_by_point(point=point)
        if not region:
            raise UnsupportedRegionException
        return region

    @staticmethod
    def validate_country_is_active(*, country: Country) -> None:
        if not country.is_active:
            raise InactiveCountryException

    @staticmethod
    def validate_user_country_match(*, region: Region, user: User) -> None:
        if not LocationSelector.is_region_country_match_user(region, user):
            raise RegionCountryMismatchException

    @staticmethod
    def validate_country_for_address(*, country: Country, point: Point) -> None:
        """
        Validate that the country is suitable for creating/updating an address.
        Checks:
        1. Always check that the country is active
        2. If ENABLE_REGION_VALIDATION is enabled, validate point is inside a region of that country

        Note: If no region boundaries exist, validation relies on client-provided country.
        """
        # Always validate country is active
        RegionValidator.validate_country_is_active(country=country)

        if config.ENABLE_REGION_VALIDATION:
            # Try to verify the point is inside a region of that country
            region = RegionSelector.get_region_by_point(point=point)

            if region:
                # If region exists, verify it matches the provided country
                if region.country.code != country.code:
                    raise UnsupportedRegionException
            # If no region found, we trust the client-provided country
            # This happens when region boundaries haven't been loaded yet
