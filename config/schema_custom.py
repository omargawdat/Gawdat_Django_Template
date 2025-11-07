from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiParameter
from drf_standardized_errors.openapi import AutoSchema


class CustomAutoSchema(AutoSchema):
    """Custom AutoSchema that adds global parameters to all endpoints."""

    global_params = [
        OpenApiParameter(
            name="Accept-Language",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
            required=False,
            description="Language preference for the response",
            examples=[
                OpenApiExample(
                    name="English (US)",
                    value="en",
                    description="English with US locale preference",
                ),
                OpenApiExample(
                    name="Arabic",
                    value="ar",
                    description="Arabic language preference",
                ),
            ],
        ),
    ]

    def get_override_parameters(self):
        """Add global parameters to all endpoints."""
        return super().get_override_parameters() + self.global_params
