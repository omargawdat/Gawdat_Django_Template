from rest_framework import permissions

from apps.users.models.customer import Customer


class IsCustomer(permissions.BasePermission):
    message = "Access denied. Only customers can access this endpoint."

    def has_permission(self, request, view):
        return isinstance(request.user, Customer)
