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
    django_admin_url: str
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
        return f"postgis://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}"

    # AWS Settings
    s3_bucket_name: str
    aws_region_name: str

    # External Services
    google_application_credentials: str
    api_key: SecretStr

    # Payment
    taps_secret_key: SecretStr

    # SMS
    is_testing_sms: bool
    our_sms_sender_name: str
    our_sms_api_key: SecretStr
    sms_misr_username: str
    sms_misr_password: SecretStr
    sms_misr_sender: str

    # Environment
    domain_name: str
    environment: Literal["local", "development", "staging", "production"]
    sentry_sdk_dsn: str
    google_map_api_key: SecretStr

    # Email Configuration
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_use_tls: bool = True
    email_host_user: str
    email_host_password: SecretStr

    # Oauth
    google_oauth2_client_id: str
    google_oauth2_client_secret: SecretStr

    facebook_oauth2_client_id: str
    facebook_oauth2_client_secret: SecretStr

    apple_oauth2_client_id: str
    apple_oauth2_client_secret: SecretStr
    key_id: str
    team_id: str


env = EnvSettings()
