from django.http import HttpRequest

from apps.users.models.provider import Provider


class ProviderContextLogic:
    provider: Provider | None

    def __init__(self, request: HttpRequest, provider: Provider | None = None):
        self.request = request
        self.provider = provider

    @property
    def is_superuser(self) -> bool:
        return self.request.user.is_superuser

    @property
    def is_staff(self) -> bool:
        return self.request.user.is_staff

    @property
    def is_creating(self) -> bool:
        return self.provider is None

    @property
    def is_created(self) -> bool:
        return self.provider is not None
