from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from apps.channel.constants import OTPType
from apps.users.api.serializer_validations import ValidCountryPhoneNumberField


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Send OTP Customer",
            value={"phone_number": "+201234567890", "otp_type": "customer_auth"},
            request_only=True,
        ),
        OpenApiExample(
            "Send OTP Provider",
            value={"phone_number": "+201234567890", "otp_type": "provider_auth"},
            request_only=True,
        ),
    ]
)
class OTPSendSerializer(serializers.Serializer):
    phone_number = ValidCountryPhoneNumberField()
    otp_type = serializers.ChoiceField(choices=OTPType.choices)
