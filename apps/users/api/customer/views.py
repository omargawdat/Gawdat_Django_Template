import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.customer.serializers import CustomerDetailedSerializer
from apps.users.api.customer.serializers import CustomerSetupSerializer
from apps.users.api.customer.serializers import CustomerUpdateSerializer
from apps.users.domain.services.user import UserServices

logger = logging.getLogger(__name__)


def _get_customer_or_404(user):
    """Get customer profile or raise 404."""
    try:
        return user.customer
    except ObjectDoesNotExist:
        raise Http404("No customer profile found for this user.") from None


class CustomerDetailView(APIView):
    """Get customer profile."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Customer"],
        operation_id="GetCustomerProfile",
        description="Retrieve the authenticated customer's complete profile including user auth data.",
        responses={
            200: CustomerDetailedSerializer,
            404: OpenApiResponse(description="Customer profile not found"),
        },
    )
    def get(self, request):
        """Get customer profile with flattened user auth fields."""
        customer = _get_customer_or_404(request.user)
        serializer = CustomerDetailedSerializer(customer, context={"request": request})
        return Response(serializer.data)


class CustomerUpdateView(APIView):
    """Update customer profile."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Customer"],
        operation_id="UpdateCustomerProfile",
        description="Update the authenticated customer's profile information.",
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
        request={
            "multipart/form-data": CustomerUpdateSerializer,
        },
        responses={
            200: CustomerDetailedSerializer,
            400: OpenApiResponse(
                description="Validation Error",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Validation Error",
                        value={
                            "field_name": ["Error message for this field"],
                            "image": ["File size should not exceed 5MB"],
                        },
                        response_only=True,
                    )
                ],
            ),
            404: OpenApiResponse(description="Customer profile not found"),
        },
    )
    def patch(self, request):
        """Update customer profile (handles both User and Customer fields)."""
        customer = _get_customer_or_404(request.user)
        serializer = CustomerUpdateSerializer(
            customer, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            CustomerDetailedSerializer(customer, context={"request": request}).data
        )


class CustomerDeleteView(APIView):
    """Delete customer account."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Customer"],
        operation_id="DeleteCustomerAccount",
        description="Deactivate the authenticated customer's account and logout from all devices.",
        responses={
            204: OpenApiResponse(description="Account successfully deactivated."),
            404: OpenApiResponse(description="Customer profile not found"),
        },
    )
    def delete(self, request):
        """Deactivate customer account and logout from all devices."""
        customer = _get_customer_or_404(request.user)
        customer.user.is_active = False
        UserServices.user_logout_all_devices(customer.user)
        customer.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerSetupView(APIView):
    """Complete customer profile after signup."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Customer"],
        operation_id="CompleteCustomerProfile",
        request=CustomerSetupSerializer,
        responses={
            201: CustomerDetailedSerializer,
            400: {"description": "Validation error or profile already completed"},
        },
    )
    def post(self, request):
        """Complete Customer profile after email verification."""
        from apps.users.domain.services.customer import CustomerService

        if hasattr(request.user, "customer"):
            return Response(
                {"error": "Profile already completed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CustomerSetupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract device data from nested serializer
        device_data = serializer.validated_data.get("device") or {}

        # Use CustomerService for business logic
        user = CustomerService.complete_customer_profile(
            user=request.user,
            country=serializer.validated_data["country"],
            language=serializer.validated_data.get("language"),
            fcm_token=device_data.get("registration_id"),
            device_id=device_data.get("device_id"),
            device_type=device_data.get("type"),
        )

        response_serializer = CustomerDetailedSerializer(
            user.customer, context={"request": request}
        )

        logger.info(f"Customer profile created for user {user.email}")

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
