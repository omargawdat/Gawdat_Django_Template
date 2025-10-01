from django.core.exceptions import ValidationError
from phonenumbers import PhoneNumber

from apps.location.domain.selector.country import CountrySelector
from apps.location.errors import LocationError
from apps.location.models.country import Country
from apps.users.fields.customer import CustomerFields


class CountryValidator:
    @staticmethod
    def validate_match_country_phone(*, phone_number: PhoneNumber, country: Country):
        return  # todo: pass this validation until finsihging the country code
        phone_country = CountrySelector.country_by_phone(phone_number)
        if phone_country != country:
            raise ValidationError(
                {
                    f"{CustomerFields.PHONE_NUMBER}": ValidationError(
                        LocationError.COUNTRY_PHONE_NUMBER.message,
                        code=LocationError.COUNTRY_PHONE_NUMBER.code,
                    )
                }
            )
