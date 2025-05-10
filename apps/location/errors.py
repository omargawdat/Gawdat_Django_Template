from common.error_codes import ErrorCode


class LocationError:
    COUNTRY_PHONE_NUMBER = ErrorCode(
        code="country_miss_match",
        message="Phone number does not match the customer's country!",
    )
    CANNOT_DELETE_PRIMARY_ADDRESS = ErrorCode(
        code="cannot_delete_primary_address",
        message="Cannot delete primary address!",
    )
