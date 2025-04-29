from django.urls import path

from apps.users.api.customer.views import CustomerAuthView
from apps.users.api.customer.views import CustomerDeleteView
from apps.users.api.customer.views import CustomerDetailView
from apps.users.api.customer.views import CustomerUpdateView

urlpatterns = [
    path(
        "customer/authenticate/",
        CustomerAuthView.as_view(),
        name="customer-authenticate",
    ),
    path("customer/update/", CustomerUpdateView.as_view(), name="customer-update"),
    path("customer/delete/", CustomerDeleteView.as_view(), name="customer-delete"),
    path("customer/me/", CustomerDetailView.as_view(), name="customer-detail"),
]
