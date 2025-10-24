from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed
        return hasattr(request.user, "customer")
