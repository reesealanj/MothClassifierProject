from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from jobs.models import Job
from ml_models.models import MLModel
from ml_models.serializers import MLModelSerializer, MLModelUpdateSerializer


class MLModelList(generics.ListCreateAPIView):
    """
    General View Description

    get: Returns a list of the machine learning models in the system
        <br>**Permissions**: Admin
        
    post: Registers a machine learning model with the system
        <br>**Permissions**: Admin
    """

    permission_classes = [IsAdminUser]
    queryset = MLModel.objects.order_by('-rating')
    serializer_class = MLModelSerializer
    filterset_fields = [
        'name',
        'date_created',
        'model_type',
        'rating',
    ]
    ordering_fields = [
        'id',
        'name',
        'date_created',
        'model_type',
        'rating',
    ]


class MLModelListByJob(generics.ListAPIView):
    """
    General View Description

    get: Returns a list of machine learning models associated with the specified job
        <br>**Permissions**: Admin
    """

    permission_classes = [IsAdminUser]
    serializer_class = MLModelSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return MLModel.objects.none()

        job = Job.objects.get(pk=self.kwargs.get('pk'))
        return job.models.all().order_by('-rating')


class MLModelDetail(generics.RetrieveUpdateAPIView):
    """
    General View Description

    get: Returns a machine learning model with the specified id
        <br>**Permissions**: Admin

    put: Updates the information for the specified machine learning model
        <br>**Permissions**: Admin

    patch: Updates the information for the specified machine learning model
        <br>**Permissions**: Admin
    """

    permission_classes = [IsAdminUser]
    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MLModelUpdateSerializer
        return self.serializer_class
