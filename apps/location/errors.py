from common.error_codes import ErrorCode


class LocationError:
    COUNTRY_PHONE_NUMBER = ErrorCode(
        code="country_miss_match",
        message="Phone number does not match the customer's country!",
    )
