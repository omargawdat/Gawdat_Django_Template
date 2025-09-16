import base64
import json

from firebase_admin import credentials
from firebase_admin import initialize_app

from config.helpers.env import env

firebase_encoded_64 = env.firebase_credentials_b64.get_secret_value()
if firebase_encoded_64 != "dummy.env":  # to avoid error when building using dummy env
    json_bytes = base64.b64decode(firebase_encoded_64)
    cred = credentials.Certificate(json.loads(json_bytes))
    FIREBASE_APP = initialize_app(cred)

FCM_DJANGO_SETTINGS = {
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
}
