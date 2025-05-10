from apps.cart.models.cart import Cart
from apps.cart.models.cart_item import CartItem
from apps.products.models.product import Product


class CartItemService:
    @staticmethod
    def create_cart_item(*, cart: Cart, product: Product, quantity) -> CartItem:
        return CartItem.objects.create(cart=cart, product=product, quantity=quantity)
