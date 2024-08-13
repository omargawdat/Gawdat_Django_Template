from phonenumber_field.modelfields import PhoneNumberField

from apps.users.domain.utilities.phone import PhoneUtils
from apps.users.helpers.constants import SupportedCountry


class PhoneValidator:
    @staticmethod
    def is_phone_in_working_country(phone_number: PhoneNumberField) -> bool:
        return PhoneUtils.get_country_iso(phone_number) in SupportedCountry.values
