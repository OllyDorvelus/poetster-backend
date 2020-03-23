from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser


class OwnerPermission(permissions.BasePermission):
    """Allow users write to their own resources only"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own resource"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id