from django.http import HttpRequest

from apps.users.models.customer import Customer


class CustomerContextLogic:
    customer: Customer | None

    def __init__(self, request: HttpRequest, customer: Customer | None = None):
        self.request = request
        self.customer = customer

    @property
    def is_superuser(self) -> bool:
        return self.request.user.is_superuser

    @property
    def is_staff(self) -> bool:
        return self.request.user.is_staff

    @property
    def is_creating(self) -> bool:
        return self.customer is None

    @property
    def is_created(self) -> bool:
        return self.customer is not None
