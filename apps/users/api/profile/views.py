"""Views for customer profile completion flow."""

import logging

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.api.user.serializers import UserWithProfileSerializer

from .serializers import CustomerProfileCompletionSerializer

logger = logging.getLogger(__name__)


class CustomerProfileCompletionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Profile"],
        operation_id="CompleteCustomerProfile",
        request=CustomerProfileCompletionSerializer,
        responses={
            201: UserWithProfileSerializer,
            400: {"description": "Validation error or profile already completed"},
        },
    )
    def post(self, request):
        """Complete Customer profile."""
        from apps.users.domain.services.customer import CustomerService

        if hasattr(request.user, "customer"):
            return Response(
                {"error": "Profile already completed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CustomerProfileCompletionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract device data from nested serializer
        device_data = serializer.validated_data.get("device") or {}

        # Use CustomerService for business logic
        user = CustomerService.complete_customer_profile(
            user=request.user,
            country=serializer.validated_data["country"],
            phone_number=serializer.validated_data.get("phone_number"),
            language=serializer.validated_data.get("language"),
            fcm_token=device_data.get("registration_id"),
            device_id=device_data.get("device_id"),
            device_type=device_data.get("type"),
        )

        response_serializer = UserWithProfileSerializer(user)

        logger.info(f"Customer profile created for user {user.email}")

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ProfileStatusView(APIView):
    """Check if user's profile is complete."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Profile"],
        operation_id="GetProfileStatus",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "is_profile_complete": {"type": "boolean"},
                },
            }
        },
        description="Check if user has completed profile setup.",
    )
    def get(self, request):
        """Get profile completion status."""
        return Response(
            {
                "is_profile_complete": request.user.is_profile_complete,
            }
        )
