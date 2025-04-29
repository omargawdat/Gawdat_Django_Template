from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.data_class import TokenData
from apps.users.models import User


class TokenService:
    @staticmethod
    def generate_token_for_user(user: User) -> TokenData:
        refresh_token = RefreshToken.for_user(user)
        return TokenData(
            access=str(refresh_token.access_token),
            refresh=str(refresh_token),
        )

    @staticmethod
    def blacklist_token(refresh_token):
        token = RefreshToken(refresh_token)
        token.blacklist()
