from django.urls import path

from .views import WalletDetailAPI
from .views import WalletRechargeAPIView
from .views import WalletUpdateView

urlpatterns = [
    path("wallets/recharge/", WalletRechargeAPIView.as_view(), name="wallet-recharge"),
    path("wallets/me/", WalletDetailAPI.as_view(), name="wallet-detail"),
    path("wallets/me/update/", WalletUpdateView.as_view(), name="wallet-update"),
]
