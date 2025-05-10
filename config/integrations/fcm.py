from firebase_admin import initialize_app

FIREBASE_APP = initialize_app()

FCM_DJANGO_SETTINGS = {
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
}
