from django.db.models import QuerySet

from apps.products.models.banner import Banner


class BannerSelector:
    @staticmethod
    def get_banners() -> QuerySet[Banner]:
        return Banner.objects.all()
