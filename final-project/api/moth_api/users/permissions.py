from fcm_django.models import FCMDevice
from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import User, ResearcherRequest


# Determines if the current user is the user corresponding to the view
class IsSelf(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(uid=view.kwargs.get('uid'))
        return request.user and request.user.is_authenticated and request.user == user

    def has_object_permission(self, request, view, obj):
        return obj == request.user


# Determines if the current user is the user corresponding to the device
class IsOwnerOfDevice(BasePermission):
    def has_permission(self, request, view):
        device = FCMDevice.objects.get(id=view.kwargs.get('pk'))
        return (
            request.user
            and request.user.is_authenticated
            and request.user == device.user
        )

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# Determines if the current user is the user corresponding to the researcher request
class IsOwnerOfResearcherRequest(BasePermission):
    def has_permission(self, request, view):
        researcher_request = ResearcherRequest.objects.get(id=view.kwargs.get('pk'))
        return (
            request.user
            and request.user.is_authenticated
            and request.user == researcher_request.user
        )

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
