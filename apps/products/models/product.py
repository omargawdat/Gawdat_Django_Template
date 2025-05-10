from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from apps.products.models.category import Category


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = MoneyField(max_digits=14, decimal_places=2, verbose_name=_("Price"))
    image = ProcessedImageField(
        upload_to="products/",
        processors=[ResizeToFit(1200, 800)],
        options={"quality": 90, "optimize": True},
        verbose_name=_("Image"),
    )

    def __str__(self):
        return self.name
