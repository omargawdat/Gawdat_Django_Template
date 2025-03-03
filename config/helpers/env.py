from typing import Annotated
from typing import Literal

from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    django_secret_key: SecretStr
    django_superuser_username: str
    django_superuser_password: SecretStr
    django_admin_name: str
    django_admin_email: str
    django_jwt_access_token_lifetime_minutes: Annotated[int, Field(gt=0)]
    django_jwt_refresh_token_lifetime_minutes: Annotated[int, Field(gt=0)]

    # Database Configuration
    db_host: str
    db_port: Annotated[int, Field(ge=1, le=65535)] = 5432
    db_user: str
    db_password: SecretStr
    db_name: str

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}"

    # AWS Settings
    s3_bucket_name: str
    aws_region_name: str

    # External Services
    google_application_credentials: str
    api_key: SecretStr
    taps_secret_key: SecretStr

    # Environment
    domain_name: str
    environment: Literal["local", "development", "staging", "production"]
    sentry_sdk_dsn: str


env = EnvSettings()
