from django.core.exceptions import ValidationError
from phonenumbers import PhoneNumber

from apps.location.domain.selector.country import CountrySelector
from apps.location.errors import LocationError
from apps.location.models.country import Country


class CountryValidator:
    @staticmethod
    def validate_match_country_phone(*, phone_number: PhoneNumber, country: Country):
        phone_country = CountrySelector.country_by_phone(phone_number)
        if phone_country != country:
            raise ValidationError(
                {
                    "phone_number": ValidationError(
                        LocationError.COUNTRY_PHONE_NUMBER.message,
                        code=LocationError.COUNTRY_PHONE_NUMBER.code,
                    )
                }
            )
