from django.urls import path

from apps.payment.api.callback.views import BankCallbackAPI
from apps.payment.api.callback.views import redirect_url
from apps.payment.api.callback.views import status_page

urlpatterns = [
    path("redirect_url/", redirect_url, name="payment-done"),
    path("redirect_url/status/", status_page, name="payment_status"),
    path("bank-callback-checkout/", BankCallbackAPI.as_view(), name="bank-callback"),
]
