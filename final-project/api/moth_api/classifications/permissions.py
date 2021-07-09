from rest_framework.permissions import BasePermission, SAFE_METHODS


# Determines if the current user is a researcher
# Otherwise, the permission is set to read only
class IsResearcherOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_researcher
            or request.method in SAFE_METHODS
        )
