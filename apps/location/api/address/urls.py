from django.urls import path

from . import views

urlpatterns = [
    path("addresses/", views.AddressListView.as_view(), name="address-list"),
    path("address/create/", views.AddressCreateView.as_view(), name="address-create"),
    path(
        "address/<int:pk>/update/",
        views.AddressUpdateView.as_view(),
        name="address-update",
    ),
    path(
        "address/<int:pk>/delete/",
        views.AddressDeleteView.as_view(),
        name="address-delete",
    ),
]
