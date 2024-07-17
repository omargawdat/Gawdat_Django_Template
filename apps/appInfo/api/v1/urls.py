from django.urls import path

from apps.appInfo.api.v1.views import AboutUsAPIView
from apps.appInfo.api.v1.views import SocialAccountsAPIView
from apps.appInfo.api.v1.views import TermsAndConditionsAPIView

urlpatterns = [
    path("social-accounts/", SocialAccountsAPIView.as_view(), name="social-accounts"),
    path("about-us/", AboutUsAPIView.as_view(), name="about-us"),
    path("terms-and-conditions/", TermsAndConditionsAPIView.as_view(), name="terms-and-conditions"),
]
