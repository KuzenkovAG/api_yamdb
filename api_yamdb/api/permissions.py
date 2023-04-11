from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAdminPermission(permissions.BasePermission):
    """Check is admin."""
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'admin'
