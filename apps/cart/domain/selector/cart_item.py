from django.db.models import QuerySet

from apps.cart.models.cart_item import CartItem
from apps.users.models.customer import Customer


class CartItemSelector:
    @staticmethod
    def get_cart_items(customer: Customer) -> QuerySet[CartItem]:
        return CartItem.objects.filter(cart__customer=customer)
