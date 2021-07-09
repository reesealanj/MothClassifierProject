from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from images.models import Image
from images.permissions import IsOwnerOfImage
from jobs.models import Job
from jobs.permissions import IsOwnerOfJob
from jobs.serializers import JobSerializer
from jobs.services import handle_job


class JobList(generics.ListAPIView):
    """
    General View Description

    get: Returns a list of the jobs in the system
        <br>**Permissions**: Admin
    """

    permission_classes = [IsAdminUser]
    queryset = Job.objects.order_by('-id')
    serializer_class = JobSerializer
    filterset_fields = [
        'job_type',
        'date_issued',
        'last_modified',
        'status',
    ]
    ordering_fields = [
        'id',
        'date_issued',
        'last_modified',
        'status',
    ]


class JobListByImage(JobList, generics.ListCreateAPIView):
    """
    General View Description

    get: Returns a list of jobs associated with the specified image
        <br>**Permissions**: Owner of Image, Admin
        
    post: Submits a job associated with the specified image
        <br>**Permissions**: Owner of Image, Admin
    """

    permission_classes = [IsOwnerOfImage | IsAdminUser]

    def get_queryset(self):
        image = Image.objects.get(id=self.kwargs.get('pk'))
        return Job.objects.filter(image=image).order_by('-id')

    def post(self, request, *args, **kwargs):
        # Job actions
        response = self.create(request, *args, **kwargs)
        handle_job.delay(response.data.get('id'))
        return response

    # Override this function to extract the image id from the url
    def get_serializer_context(self):
        context = super(JobListByImage, self).get_serializer_context()
        context.update({'image_id': self.kwargs.get('pk')})

        return context


class JobDetail(generics.RetrieveAPIView):
    """
    General View Description

    get: Returns a job with the specified id
        <br>**Permissions**: Owner of Job, Admin
    """

    permission_classes = [IsOwnerOfJob | IsAdminUser]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
