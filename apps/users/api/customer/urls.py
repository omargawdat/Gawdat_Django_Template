from django.urls import path

from apps.users.api.customer.views import CustomerDeleteView
from apps.users.api.customer.views import CustomerDetailView
from apps.users.api.customer.views import CustomerUpdateView

urlpatterns = [
    path("customers/me/", CustomerDetailView.as_view(), name="customer-detail"),
    path("customers/me/update/", CustomerUpdateView.as_view(), name="customer-update"),
    path("customers/me/delete/", CustomerDeleteView.as_view(), name="customer-delete"),
]
