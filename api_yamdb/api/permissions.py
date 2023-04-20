from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """Check is admin."""
    def has_permission(self, request, view):
        return request.user.is_admin


class IsModeratorPermission(permissions.BasePermission):
    """Check is moderator."""
    def has_permission(self, request, view):
        return request.user.is_moderator


class IsAuthorPermission(permissions.BasePermission):
    """Check is author."""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class AdminOrModeratorOrAuthorPermission(permissions.BasePermission):
    """Permission is granted to check the access rights
      of the author, admin and moderator."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminOrReadPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )
