from django.urls import path

from .views import TransactionsView

urlpatterns = [
    path("transactions/", TransactionsView.as_view(), name="transactions"),
]
