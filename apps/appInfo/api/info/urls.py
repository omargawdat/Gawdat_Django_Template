from django.urls import path

from apps.appInfo.api.info.views import AppInfoAPIView
from apps.appInfo.api.info.views import FAQListView
from apps.appInfo.api.info.views import SocialAccountsAPIView

urlpatterns = [
    path("social-accounts/", SocialAccountsAPIView.as_view(), name="social-accounts"),
    path("info/", AppInfoAPIView.as_view(), name="app-info"),
    path("faqs/", FAQListView.as_view(), name="faqs"),
]
