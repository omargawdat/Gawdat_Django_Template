from django.utils.translation import gettext_lazy as _


class ErrorCode:
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message


class ApplicationError:
    OVERLAPPING_EVENTS = ErrorCode(
        code="overlapping_events", message=_("Events cannot overlap.")
    )
    CAPACITY_TOO_LOW = ErrorCode(
        code="capacity_gte_1", message=_("Capacity must be greater than or equal to 1.")
    )

    @classmethod
    def get_message(cls, code: str) -> str | None:
        error_map = {
            value.code: value.message
            for key, value in vars(cls).items()
            if isinstance(value, ErrorCode)
        }
        return error_map.get(code)
