from django.db.models import QuerySet

from apps.products.models.category import Category


class CategorySelector:
    @staticmethod
    def get_categories() -> QuerySet[Category]:
        return Category.objects.all()
