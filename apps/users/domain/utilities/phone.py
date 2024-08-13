import phonenumbers
from phonenumber_field.modelfields import PhoneNumberField


class PhoneUtils:
    @staticmethod
    def get_country_iso(phone_number: PhoneNumberField) -> str:
        parsed_phone = phonenumbers.parse(str(phone_number))
        return phonenumbers.region_code_for_number(parsed_phone)
