from rest_framework import permissions


class AdminWrite(permissions.BasePermission):
    """Only admin can change resource, others will be able to view"""

    def has_object_permission(self, request, view, obj):
        """"Check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser


class OwnerPermission(permissions.BasePermission):
    """Allow users write to their own resources only"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update thier own status"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user.id