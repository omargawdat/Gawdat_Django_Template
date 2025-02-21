from typing import Annotated
from typing import Literal

from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    django_secret_key: SecretStr = Field(..., min_length=20)
    django_superuser_username: str
    django_superuser_password: SecretStr
    django_admin_name: str
    django_admin_email: str
    django_jwt_access_token_lifetime_minutes: Annotated[int, Field(gt=0)]
    django_jwt_refresh_token_lifetime_minutes: Annotated[int, Field(gt=0)]

    # Database Configuration
    postgres_host: str
    postgres_port: Annotated[int, Field(ge=1, le=65535)] = 5432
    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password.get_secret_value()}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    # AWS Settings
    aws_storage_bucket_name: str
    aws_region_name: str

    # External Services
    google_application_credentials: str
    api_key: SecretStr
    taps_secret_key: SecretStr

    # Environment
    domain_name: str
    environment: Literal["local", "development", "staging", "production"]
    sentry_sdk_dsn: str
