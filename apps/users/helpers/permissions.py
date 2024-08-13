from rest_framework import permissions

from apps.users.models.customer import Customer
from apps.users.models.provider import Provider


class IsActiveCustomer(permissions.BasePermission):
    message = "Access denied."

    def has_permission(self, request, view):
        if not isinstance(request.user, Customer):
            self.message = "This endpoint is for customers only."
            return False

        if not request.user.is_phone_verified:
            self.message = "Phone number verification required."
            return False
        return True


class IsActiveProvider(permissions.BasePermission):
    message = "Access denied."

    def has_permission(self, request, view):
        if not isinstance(request.user, Provider):
            self.message = "This endpoint is for providers only."
            return False

        if not request.user.is_phone_verified:
            self.message = "Phone number verification required."
            return False
        return True
