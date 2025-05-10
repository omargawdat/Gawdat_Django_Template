from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.channel.api.sms.serializers import OTPSendSerializer
from apps.channel.domain.services.otp import OTPUtils


class OTPSendView(APIView):
    permission_classes = []
    serializer_class = OTPSendSerializer

    def post(self, request, *args, **kwargs):
        serializer = OTPSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        OTPUtils.send_otp(
            phone_number=serializer.validated_data["phone_number"],
            otp_type=serializer.validated_data["otp_type"],
        )

        return Response({"message": "OTP has been sent"}, status=status.HTTP_200_OK)
