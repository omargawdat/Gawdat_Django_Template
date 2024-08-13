from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import serializers

from .serializers import CustomerLoginSerializer
from .serializers import CustomerOutputSerializer
from .serializers import CustomerRegisterSerializer


class ErrorResponseSerializer(serializers.Serializer):
    field_name = serializers.ListField(child=serializers.CharField())


customer_register_swagger = extend_schema(
    request=CustomerRegisterSerializer,
    responses={
        201: OpenApiResponse(
            response=CustomerOutputSerializer,
            description="Customer registered successfully",
        ),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Invalid input data"),
    },
    description="Register a new customer. Note: Phone number should include the country code (e.g., +966 for SA).",
    summary="Customer Registration",
    tags=["Customer"],
)

customer_login_swagger = extend_schema(
    request=CustomerLoginSerializer,
    responses={
        200: OpenApiResponse(
            response=CustomerOutputSerializer,
            description="Customer logged in successfully",
        ),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Invalid credentials"),
    },
    description="Login for customers.",
    summary="Customer Login",
    tags=["Customer"],
)
