from django.urls import path

from apps.users.api.customer.views import CustomerDetailView
from apps.users.api.customer.views import CustomerLoginView
from apps.users.api.customer.views import CustomerRegistrationView

urlpatterns = [
    path("v1/customer/register/", CustomerRegistrationView.as_view(), name="customer-register"),
    path("v1/customer/login/", CustomerLoginView.as_view(), name="customer-login"),
    path("v1/customer/me/", CustomerDetailView.as_view(), name="customer-detail"),
]
