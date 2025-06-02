from drf_spectacular.utils import extend_schema
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
        tags=["User/Common"],
        operation_id="sendOTP",
        request={
            "application/json": OTPSendSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = OTPSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        OTPUtils.send_otp(
            phone_number=serializer.validated_data["phone_number"],
            otp_type=serializer.validated_data["otp_type"],
        )

        return Response(status=status.HTTP_200_OK)
