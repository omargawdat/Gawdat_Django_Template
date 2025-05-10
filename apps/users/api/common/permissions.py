from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models.customer import Customer


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed
        return isinstance(request.user, Customer)
