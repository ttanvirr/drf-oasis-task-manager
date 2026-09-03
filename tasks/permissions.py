from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission that allows only the owner or a superuser to access an object.

    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Access allowed if
        # current user = owner of the requested object or a superuser.
        return request.user.is_superuser or obj.owner == request.user
