import base64
import json

from firebase_admin import credentials
from firebase_admin import initialize_app

from config.helpers.env import env


def _get_firebase_credentials():
    """
    Decode base64-encoded Firebase credentials and create a credential object.
    """
    # Decode base64 string to JSON
    credentials_json = base64.b64decode(env.firebase_credentials_b64.get_secret_value())
    credentials_dict = json.loads(credentials_json)

    # Create Firebase credentials from dictionary
    return credentials.Certificate(credentials_dict)


FIREBASE_APP = initialize_app(_get_firebase_credentials())

FCM_DJANGO_SETTINGS = {
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
}
