from django.utils.translation import gettext_lazy as _

from common.error_codes import ErrorCode


class OTPError:
    RATE_LIMIT_EXCEEDED = ErrorCode(
        "OTP-001", _("Hourly OTP limit exceeded. Please try again later.")
    )
    SEND_FAILURE = ErrorCode("OTP-002", _("Failed to send verification code"))
    GENERAL_ERROR = ErrorCode("OTP-003", _("Error sending code"))
    OTP_NOT_FOUND = ErrorCode("OTP-004", _("Verification code expired or not found"))
    MAX_ATTEMPTS_EXCEEDED = ErrorCode(
        "OTP-005", _("Maximum verification attempts exceeded")
    )
    INVALID_CODE = ErrorCode("OTP-006", _("Invalid verification code"))
