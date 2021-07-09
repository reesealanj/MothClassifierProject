from rest_framework.permissions import BasePermission

from jobs.models import Job


# Determines if the current user is the user corresponding to the job
class IsOwnerOfJob(BasePermission):
    def has_permission(self, request, view):
        job = Job.objects.get(id=view.kwargs.get('pk'))
        return (
            request.user
            and request.user.is_authenticated
            and request.user == job.image.user
        )

    def has_object_permission(self, request, view, obj):
        return obj.image.user == request.user
