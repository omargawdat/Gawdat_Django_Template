import base64
import json
import logging

from firebase_admin import credentials
from firebase_admin import initialize_app

from config.helpers.env import env

logger = logging.getLogger(__name__)


def _get_firebase_credentials():
    """
    Decode base64-encoded Firebase credentials and create a credential object.
    """
    # Decode base64 string to JSON
    credentials_json = base64.b64decode(env.firebase_credentials_b64.get_secret_value())
    credentials_dict = json.loads(credentials_json)

    # Create Firebase credentials from dictionary
    return credentials.Certificate(credentials_dict)


def _initialize_firebase():
    """
    Initialize Firebase app with error handling for dummy/invalid credentials.
    Returns None if initialization fails (e.g., in development with dummy credentials).
    """
    try:
        return initialize_app(_get_firebase_credentials())
    except (ValueError, KeyError) as e:
        logger.warning(
            f"Firebase initialization failed: {e}. "
            "This is expected with dummy credentials. FCM notifications will not work."
        )
        return None


FIREBASE_APP = _initialize_firebase()

FCM_DJANGO_SETTINGS = {
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
}
