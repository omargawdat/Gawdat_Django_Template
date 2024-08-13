from django.urls import path

from apps.users.api.provider.views import ProviderDetailView
from apps.users.api.provider.views import ProviderLoginView
from apps.users.api.provider.views import ProviderRegistrationView

urlpatterns = [
    path("v1/provider/register/", ProviderRegistrationView.as_view(), name="customer-register"),
    path("v1/provider/login/", ProviderLoginView.as_view(), name="provider-login"),
    path("v1/provider/me/", ProviderDetailView.as_view(), name="provider-detail"),
]
