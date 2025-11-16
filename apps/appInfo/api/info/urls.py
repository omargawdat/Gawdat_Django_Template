from django.urls import path

from apps.appInfo.api.info.views import AppInfoAPIView
from apps.appInfo.api.info.views import ContactUsCreateView
from apps.appInfo.api.info.views import FAQListView
from apps.appInfo.api.info.views import OnboardingAPIView
from apps.appInfo.api.info.views import SocialAccountsAPIView

urlpatterns = [
    path("social-accounts/", SocialAccountsAPIView.as_view(), name="social-accounts"),
    path("info/", AppInfoAPIView.as_view(), name="app-info"),
    path("faqs/", FAQListView.as_view(), name="faqs"),
    path("contact-us/", ContactUsCreateView.as_view(), name="contact-us"),
    path("test-atomic/", FAQAtomicTestView.as_view(), name="test-atomic"),
    path("onboarding/", OnboardingAPIView.as_view(), name="onboarding"),

]
