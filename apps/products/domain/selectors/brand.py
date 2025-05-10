from django.db.models import QuerySet

from apps.products.models.brand import Brand


class BrandSelector:
    @staticmethod
    def get_brands() -> QuerySet[Brand]:
        return Brand.objects.all()
