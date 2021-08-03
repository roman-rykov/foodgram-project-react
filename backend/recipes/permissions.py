from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """
    Can edit its own objects
    """
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            return bool(obj.author == request.user)
        return False


class IsAdmin(permissions.BasePermission):
    """
    Can add and edit any objects
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)


class ReadOnly(permissions.BasePermission):
    """
    Can view objects
    """
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return bool(request.method in permissions.SAFE_METHODS)


class IsAuthenticated(permissions.BasePermission):
    """
    Can add new objects
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return False
