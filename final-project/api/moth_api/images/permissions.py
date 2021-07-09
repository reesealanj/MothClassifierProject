from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)

from images.models import Image


# Determines if the current user is the user corresponding to the image
class IsOwnerOfImage(BasePermission):
    def has_permission(self, request, view):
        image = Image.objects.get(id=view.kwargs.get('pk'))
        return (
            request.user
            and request.user.is_authenticated
            and request.user == image.user
        )

    def has_object_permission(self, request, view, obj):
        try:
            return obj.user == request.user or request.method in SAFE_METHODS
        except AttributeError:
            return obj.image.user == request.user or request.method in SAFE_METHODS
