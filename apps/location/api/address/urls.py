from django.urls import path

from . import views

urlpatterns = [
    path("addresses/", views.AddressListView.as_view(), name="address-list"),
    path("addresses/create/", views.AddressCreateView.as_view(), name="address-create"),
    path(
        "addresses/<int:pk>/update/",
        views.AddressUpdateView.as_view(),
        name="address-update",
    ),
    path(
        "addresses/<int:pk>/delete/",
        views.AddressDeleteView.as_view(),
        name="address-delete",
    ),
]
