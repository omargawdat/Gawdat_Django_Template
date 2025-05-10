from django.urls import path

from .views import CartItemCreateAPIView
from .views import CartItemDeleteAPIView
from .views import CartItemListAPIView
from .views import CartItemUpdateAPIView

urlpatterns = [
    path("cart/item/list/", CartItemListAPIView.as_view(), name="cart-item-list"),
    path("cart/item/create/", CartItemCreateAPIView.as_view(), name="cart-item-create"),
    path(
        "cart/item/<int:pk>/update/",
        CartItemUpdateAPIView.as_view(),
        name="cart-item-update",
    ),
    path(
        "cart/item/<int:pk>/delete/",
        CartItemDeleteAPIView.as_view(),
        name="cart-item-delete",
    ),
]
