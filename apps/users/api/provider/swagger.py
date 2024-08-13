from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import serializers

from .serializers import ProviderLoginSerializer
from .serializers import ProviderOutputSerializer
from .serializers import ProviderRegisterSerializer


class ErrorResponseSerializer(serializers.Serializer):
    field_name = serializers.ListField(child=serializers.CharField())


provider_register_swagger = extend_schema(
    request=ProviderRegisterSerializer,
    responses={
        201: OpenApiResponse(
            response=ProviderOutputSerializer,
            description="Provider registered successfully",
        ),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Invalid input data"),
    },
    description="Register a new provider. Note: Phone number should include the country code (e.g., +966 for SA).",
    summary="Provider Registration",
    tags=["Provider"],
)

provider_login_swagger = extend_schema(
    request=ProviderLoginSerializer,
    responses={
        200: OpenApiResponse(
            response=ProviderOutputSerializer,
            description="Provider logged in successfully",
        ),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Invalid credentials"),
    },
    description="Login for providers.",
    summary="Provider Login",
    tags=["Provider"],
)
