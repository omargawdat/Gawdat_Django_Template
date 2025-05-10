from phonenumber_field.serializerfields import PhoneNumberField

from apps.users.api.common.exceptions import InvalidPhoneException
from apps.users.domain.selectors.user import UserSelector


class ValidCountryPhoneNumberField(PhoneNumberField):
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        if not UserSelector.phone_country(value):
            raise InvalidPhoneException
        return value
