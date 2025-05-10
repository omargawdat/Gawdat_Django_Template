from apps.cart.models.cart import Cart
from apps.users.models.customer import Customer


class CartService:
    @staticmethod
    def create_associated_cart(customer: Customer) -> None:
        Cart.objects.create(customer=customer)

    @staticmethod
    def get_customer_cart(customer: Customer) -> Cart:
        return Cart.objects.get(customer=customer)
