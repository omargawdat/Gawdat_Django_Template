from rest_framework import serializers

from apps.channel.constants import OTPType
from apps.users.api.common.serializer_validations import ValidCountryPhoneNumberField


class OTPSendSerializer(serializers.Serializer):
    phone_number = ValidCountryPhoneNumberField()
    otp_type = serializers.ChoiceField(choices=OTPType.choices)
