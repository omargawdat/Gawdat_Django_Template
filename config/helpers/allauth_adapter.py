from allauth.headless.adapter import DefaultHeadlessAdapter

from apps.users.api.customer.serializers import CustomerDetailedSerializer
from apps.users.api.provider.serializers import ProviderDetailedSerializer


class CustomHeadlessAdapter(DefaultHeadlessAdapter):
    """Custom adapter to include profile metadata in auth responses."""

    def serialize_user(self, user):
        """Return user data with nested detailed profile serializer."""

        # Base user data (always returned)
        data = {
            "id": user.id,
            "email": user.email,
            "language": user.language,
            "customer": (
                CustomerDetailedSerializer(user.customer).data
                if hasattr(user, "customer")
                else None
            ),
            "provider": (
                ProviderDetailedSerializer(user.provider).data
                if hasattr(user, "provider")
                else None
            ),
        }

        # Add nested profile data (null if not exists)

        return data
