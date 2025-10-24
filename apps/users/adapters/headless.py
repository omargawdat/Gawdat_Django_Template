"""Custom headless adapter for django-allauth."""

from dataclasses import dataclass
from dataclasses import field

from allauth.headless.adapter import DefaultHeadlessAdapter


@dataclass
class CustomerProfileData:
    """Customer profile data for OpenAPI schema."""

    id: int = field(metadata={"description": "Customer ID", "example": 1})
    country: str = field(
        metadata={"description": "Country name", "example": "Saudi Arabia"}
    )
    country_code: str = field(metadata={"description": "Country code", "example": "SA"})


@dataclass
class CustomUserData:
    """Custom user data with nested customer profile for OpenAPI schema."""

    # Required fields (no defaults)
    id: int = field(metadata={"description": "User ID", "example": 1})
    username: str = field(metadata={"description": "Username", "example": "user"})

    # Optional fields (with defaults)
    email: str | None = field(
        default=None,
        metadata={"description": "Email address", "example": "user@example.com"},
    )
    phone_number: str | None = field(
        default=None,
        metadata={"description": "Phone number", "example": "+966555555555"},
    )
    phone_verified: bool = field(
        default=False,
        metadata={"description": "Phone verification status", "example": False},
    )
    language: str = field(
        default="ar", metadata={"description": "Preferred language", "example": "ar"}
    )
    customer: CustomerProfileData | None = field(
        default=None,
        metadata={"description": "Customer profile data", "example": None},
    )


class CustomHeadlessAdapter(DefaultHeadlessAdapter):
    """
    Custom adapter to return user with nested customer profile.

    Overrides both get_user_dataclass() and user_as_dataclass() to ensure:
    - OpenAPI schema reflects the custom user structure
    - Runtime responses return the correct nested data
    """

    def get_user_dataclass(self):
        """Return custom user dataclass for OpenAPI schema generation."""
        return CustomUserData

    def user_as_dataclass(self, user):
        """Convert user instance to CustomUserData dataclass."""
        # Get customer profile data if exists
        customer_data = None
        if hasattr(user, "customer"):
            customer = user.customer
            customer_data = CustomerProfileData(
                id=customer.id,
                country=customer.country.name,
                country_code=customer.country.code,
            )

        # Create and return the dataclass instance
        return CustomUserData(
            id=user.id,
            username=user.username,
            email=user.email,
            phone_number=str(user.phone_number) if user.phone_number else None,
            phone_verified=user.phone_verified,
            language=user.language,
            customer=customer_data,
        )
