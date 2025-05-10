from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models.customer import Customer


class Cart(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name=_("Customer"),
    )

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return self.customer.username
