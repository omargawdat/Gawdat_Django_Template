from django.urls import path

from apps.users.api.provider.views import ProviderDeleteView
from apps.users.api.provider.views import ProviderDetailView
from apps.users.api.provider.views import ProviderSetupView
from apps.users.api.provider.views import ProviderUpdateView

urlpatterns = [
    path("providers/setup/", ProviderSetupView.as_view(), name="provider-setup"),
    path("providers/me/", ProviderDetailView.as_view(), name="provider-detail"),
    path("providers/me/update/", ProviderUpdateView.as_view(), name="provider-update"),
    path("providers/me/delete/", ProviderDeleteView.as_view(), name="provider-delete"),
]
