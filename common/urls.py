from django.urls import path

from .web_view import terms_and_policy

urlpatterns = [
    path("terms/", terms_and_policy, name="terms_and_policy"),
]
