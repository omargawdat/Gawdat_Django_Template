from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class PhoneNumberUserTypeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "phone_number": _(
            "Phone number is already registered to a user of a different type."
        )
    }
    default_code = "phone_number_user_mismatch"


class InvalidPhoneException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {"phone_number": _("Phone number is not in a working country")}
    default_code = "unsupported_phone_country"


class InactiveUserError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _(
        "User account is deactivated. Please contact support for assistance."
    )
    default_code = "inactive_user"
