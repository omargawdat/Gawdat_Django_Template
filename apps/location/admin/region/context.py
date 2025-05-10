from django.http import HttpRequest

from apps.location.models.region import Region


class RegionContextLogic:
    def __init__(self, request: HttpRequest, region: Region | None = None):
        self.request = request
        self.region = region

    @property
    def is_superuser(self) -> bool:
        return self.request.user.is_superuser

    @property
    def is_staff(self) -> bool:
        return self.request.user.is_staff

    @property
    def is_creating(self) -> bool:
        return self.region is None
