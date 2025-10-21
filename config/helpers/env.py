from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # Django
    django_secret_key: SecretStr
    django_superuser_username: str
    django_superuser_password: SecretStr
    django_admin_url: str
    django_admin_name: str
    django_admin_email: str

    # Database
    database_url: str

    # Environment
    domain_name: str
    environment: Literal["local", "development", "staging", "production"]
    sentry_sdk_dsn: str

    # AWS
    s3_bucket_name: str
    aws_region_name: str

    # Firebase
    firebase_credentials_b64: SecretStr

    # Google Services
    google_map_api_key: SecretStr

    # OAuth Providers
    google_oauth2_client_id: str
    google_oauth2_client_secret: SecretStr

    # Payment
    taps_secret_key: SecretStr
    payment_confirmation_key: SecretStr

    # Payment - Paymob
    paymob_secret_key: SecretStr
    paymob_public_key: str
    paymob_card_payment_method: str
    paymob_wallet_payment_method: str

    # SMS
    is_testing_sms: bool
    our_sms_sender_name: str
    our_sms_api_key: SecretStr
    sms_misr_username: str
    sms_misr_password: SecretStr
    sms_misr_sender: str

    # Email
    email_host_user: str
    email_host_password: SecretStr

    # Frontend Configuration
    frontend_default_url: str
    frontend_allowed_origins: str

    # Cookie Configuration (for cross-domain/subdomain auth)
    # Leave empty for localhost, use ".example.com" for production subdomains
    cookie_domain: str = ""

    # Other
    api_key: SecretStr


env = EnvSettings()
