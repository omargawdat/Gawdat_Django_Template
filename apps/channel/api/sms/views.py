from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.channel.api.sms.serializers import OTPSendSerializer
from apps.channel.domain.services.otp import OTPUtils


class OTPSendView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = OTPSendSerializer

    @extend_schema(
        tags=["User/Authentication/PhoneNumber"],
        operation_id="sendOTP",
        request={"application/json": OTPSendSerializer},
        responses={
            200: inline_serializer(
                name="OTPSendResponse",
                fields={
                    "message": serializers.CharField(),
                },
            )
        },
        examples=[
            OpenApiExample(
                name="Send OTP (Customer Auth)",
                description="Request an OTP for customer authentication.",
                value={
                    "phone_number": "+966111111111",
                    "otp_type": "customer_auth",
                    "otp_auto_complete_token": "abc123xyz",
                },
                request_only=True,
            )
        ],
        description="Send an OTP to the provided phone number (or return a test message in non-SMS environments).",
    )
    def post(self, request, *args, **kwargs):
        serializer = OTPSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        OTPUtils.send_otp(
            phone_number=serializer.validated_data["phone_number"],
            otp_type=serializer.validated_data["otp_type"],
        )

        return Response(
            {"message": "OTP sent successfully."}, status=status.HTTP_200_OK
        )
