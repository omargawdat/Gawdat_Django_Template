from django.urls import path

from .views import WalletDetailAPI
from .views import WalletUpdateView

urlpatterns = [
    path("wallets/me/", WalletDetailAPI.as_view(), name="wallet-detail"),
    path("wallets/me/update/", WalletUpdateView.as_view(), name="wallet-update"),
]
