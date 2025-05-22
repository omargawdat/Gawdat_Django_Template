from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class UnsupportedRegionException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("The provided location is not in a supported region.")
    default_code = "unsupported_region"


class RegionCountryMismatchException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _(
        "The region of the provided location does not match the user's country."
    )
    default_code = "region_country_mismatch"
