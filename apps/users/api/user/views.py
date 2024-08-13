from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.user.serializers import ChangePasswordSerializer
from apps.users.api.user.serializers import PhoneNumberSerializer
from apps.users.api.user.serializers import VerifyOtpSerializer
from apps.users.domain.utilities.otp.otp_utility import OTPUtility
from apps.users.models import MobileUser


class SendOtpView(APIView):
    permission_classes = []
    serializer_class = PhoneNumberSerializer

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification_id = OTPUtility.send_otp(serializer.validated_data["phone_number"])
        return Response(
            {"message": "OTP sent successfully", "verification_id": str(verification_id)},
            status=status.HTTP_200_OK,
        )


class VerifyPhoneView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        otp = serializer.validated_data["otp"]

        if not OTPUtility.verify_otp(phone_number, otp, 0000):
            raise ValidationError("Invalid OTP")

        try:
            user = MobileUser.objects.select_for_update().get(phone_number=phone_number)
        except MobileUser.DoesNotExist as err:
            raise NotFound("User not found") from err

        user.is_phone_verified = True
        user.save()

        return Response(
            {"message": "Phone number verified successfully"}, status=status.HTTP_200_OK
        )


class VerifyPasswordForgetView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        otp = serializer.validated_data["otp"]

        if not OTPUtility.verify_otp(phone_number, otp, 0000):
            raise ValidationError("Invalid OTP")

        user = MobileUser.objects.filter(phone_number=phone_number).first()
        if not user:
            raise NotFound("User not found")

        # Generate a temporary token for password reset
        reset_token = OTPUtility.generate_reset_token(user)

        return Response(
            {"message": "OTP verified successfully", "reset_token": reset_token},
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_token = serializer.validated_data["reset_token"]
        new_password = serializer.validated_data["new_password"]

        user = OTPUtility.get_user_from_reset_token(reset_token)
        if not user:
            raise ValidationError("Invalid or expired reset token")

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Invalidate the reset token
        OTPUtility.invalidate_reset_token(reset_token)

        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


class UserDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        if not user.is_active:
            raise PermissionDenied("Account is already deactivated.")

        user.is_active = False
        user.save()
        return Response(
            {"detail": "Your account has been deactivated successfully."}, status=status.HTTP_200_OK
        )
