import logging

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.provider.serializers import ProviderDetailedSerializer
from apps.users.api.provider.serializers import ProviderSetupSerializer
from apps.users.api.provider.serializers import ProviderUpdateSerializer
from apps.users.api.user.serializers import UserWithProviderProfileSerializer
from apps.users.domain.services.user import UserServices

logger = logging.getLogger(__name__)


class ProviderDetailView(APIView):
    """Get provider profile."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Provider"],
        operation_id="GetProviderProfile",
        description="Retrieve the authenticated provider's complete profile including user auth data.",
        responses={
            200: ProviderDetailedSerializer,
        },
    )
    def get(self, request):
        """Get provider profile with flattened user auth fields."""
        provider = request.user.provider
        serializer = ProviderDetailedSerializer(provider, context={"request": request})
        return Response(serializer.data)


class ProviderUpdateView(APIView):
    """Update provider profile."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Provider"],
        operation_id="UpdateProviderProfile",
        description="Update the authenticated provider's profile information.",
        parameters=[
            OpenApiParameter(
                name="Accept-Language",
                type=OpenApiTypes.STR,
                location="header",
                required=False,
                description="Language preference for the response",
                examples=[
                    OpenApiExample(
                        name="English (US)",
                        value="en",
                        description="English with US locale preference",
                    ),
                ],
            ),
        ],
        request=ProviderUpdateSerializer,
        responses={
            200: ProviderDetailedSerializer,
            400: OpenApiResponse(
                description="Validation Error",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Validation Error",
                        value={
                            "field_name": ["Error message for this field"],
                            "company_name": ["This field is required"],
                        },
                        response_only=True,
                    )
                ],
            ),
        },
    )
    def patch(self, request):
        """Update provider profile (handles both User and Provider fields)."""
        provider = request.user.provider
        serializer = ProviderUpdateSerializer(
            provider, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            ProviderDetailedSerializer(provider, context={"request": request}).data
        )


class ProviderDeleteView(APIView):
    """Delete provider account."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Provider"],
        operation_id="DeleteProviderAccount",
        description="Deactivate the authenticated provider's account and logout from all devices.",
        responses={
            204: OpenApiResponse(description="Account successfully deactivated."),
        },
    )
    def delete(self, request):
        """Deactivate provider account and logout from all devices."""
        provider = request.user.provider
        provider.user.is_active = False
        UserServices.user_logout_all_devices(provider.user)
        provider.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProviderSetupView(APIView):
    """Complete provider profile after signup."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Provider"],
        operation_id="CompleteProviderProfile",
        request=ProviderSetupSerializer,
        responses={
            201: UserWithProviderProfileSerializer,
            400: {"description": "Validation error or profile already completed"},
        },
    )
    def post(self, request):
        """Complete Provider profile after email verification."""
        from apps.users.domain.services.provider import ProviderService

        if hasattr(request.user, "provider"):
            return Response(
                {"error": "Profile already completed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProviderSetupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract device data from nested serializer
        device_data = serializer.validated_data.get("device") or {}

        # Use ProviderService for business logic
        user = ProviderService.complete_provider_profile(
            user=request.user,
            company_name=serializer.validated_data.get("company_name"),
            language=serializer.validated_data.get("language"),
            fcm_token=device_data.get("registration_id"),
            device_id=device_data.get("device_id"),
            device_type=device_data.get("type"),
        )

        response_serializer = UserWithProviderProfileSerializer(user)

        logger.info(f"Provider profile created for user {user.email}")

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
