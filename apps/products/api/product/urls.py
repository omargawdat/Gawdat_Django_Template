from django.urls import path

from .views import ProductListView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
]
