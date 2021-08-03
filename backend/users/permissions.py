from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class CurrentUserOrAdminOrReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if bool(user.is_authenticated and obj == user):
            return True
        return bool(request.method in SAFE_METHODS or user.is_staff)
