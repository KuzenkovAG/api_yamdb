from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """Check is admin."""
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsModeratorPermission(permissions.BasePermission):
    """Check is moderator."""
    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsAuthorPermission(permissions.BasePermission):
    """Check is author."""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
