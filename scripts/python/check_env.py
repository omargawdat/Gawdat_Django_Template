import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Define environment variable requirements
REQUIRED_ENV_VARS: dict[str, list[str]] = {
    "common": [
        "DJANGO_SECRET_KEY",
        "DJANGO_SETTINGS_MODULE",
        "DJANGO_SUPERUSER_USERNAME",
        "DJANGO_SUPERUSER_PASSWORD",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "TAPS_SECRET_KEY",
        "GOOGLE_APPLICATION_CREDENTIALS",
        "JWT_ACCESS_TOKEN_LIFETIME_MINUTES",
        "JWT_REFRESH_TOKEN_LIFETIME_MINUTES",
    ],
    "local": [
        "USE_DOCKER",
        "IPYTHONDIR",
    ],
    "prod": [
        "DOMAIN_NAME",
        "TRAEFIK_EMAIL",
        "DJANGO_ADMIN_URL",
        "DJANGO_ALLOWED_HOSTS",
        "DJANGO_SECURE_SSL_REDIRECT",
        "DJANGO_AWS_ACCESS_KEY_ID",
        "DJANGO_AWS_SECRET_ACCESS_KEY",
        "DJANGO_AWS_S3_REGION_NAME",
        "DJANGO_AWS_STORAGE_BUCKET_NAME",
        "SENTRY_DSN",
    ],
}

# Define required files per environment
REQUIRED_FILES: dict[str, list[str]] = {
    "common": [
        "firebase_cred.json",
    ],
    "local": [],
    "prod": [],
}

ENVIRONMENT_NOT_SET_MESSAGE = "ENVIRONMENT is not set. Cannot determine environment."


def get_environment() -> str:
    environment = os.getenv("ENVIRONMENT")
    if not environment:
        raise OSError(ENVIRONMENT_NOT_SET_MESSAGE)
    return environment


def get_required_items(
    environment: str,
    required_map: dict[str, list[str]],
) -> list[str]:
    common_items = required_map.get("../../common", [])
    environment_items = required_map.get(environment, [])
    return common_items + environment_items


def validate_env_vars(vars_list: list[str]) -> None:
    missing_vars = [var for var in vars_list if var not in os.environ]
    if missing_vars:
        missing_vars_list = "\n - ".join(missing_vars)
        error_msg = (
            "The following environment variables are missing:\n - " + missing_vars_list
        )
        raise OSError(error_msg)
    logger.info("All required environment variables are present.")


def validate_files(files_list: list[str]) -> None:
    missing_files = [f for f in files_list if not Path(f).is_file()]
    if missing_files:
        missing_files_list = "\n - ".join(missing_files)
        error_msg = (
            "The following required files are missing:\n - " + missing_files_list
        )
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    logger.info("All required files are present.")


def run_env_validation() -> None:
    environment = get_environment()

    required_vars = get_required_items(environment, REQUIRED_ENV_VARS)
    validate_env_vars(required_vars)

    required_files = get_required_items(environment, REQUIRED_FILES)
    validate_files(required_files)
