from django.http import HttpRequest

from apps.location.models.country import Country


class CountryContextLogic:
    def __init__(self, request: HttpRequest, country: Country | None = None):
        self.request = request
        self.country = country

    @property
    def is_superuser(self) -> bool:
        return self.request.user.is_superuser

    @property
    def is_staff(self) -> bool:
        return self.request.user.is_staff

    @property
    def is_creating(self) -> bool:
        return self.country is None
