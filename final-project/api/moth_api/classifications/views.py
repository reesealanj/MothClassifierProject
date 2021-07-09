from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from classifications.models import Classification
from classifications.permissions import IsResearcherOrReadOnly
from classifications.serializers import ClassificationSerializer


class ClassificationList(generics.ListAPIView):
    """
    General View Description

    get: Returns a list of classifications in the system
        <br>**Permissions**: Public
    """

    queryset = Classification.objects.order_by('-image_id')
    serializer_class = ClassificationSerializer
    filterset_fields = [
        'species',
        'accuracy',
        'is_automated',
        'needs_review',
    ]
    ordering_fields = [
        'species',
        'accuracy',
    ]


class ClassificationDetail(generics.RetrieveUpdateAPIView):
    """
    General View Description

    get: Returns a classification of the specified image
        <br>**Permissions**: Public

    put: Updates the information for the classification of the specified image
        <br>**Permissions**: Researcher, Admin
        
    patch: Updates the information for the classification of the specified image
        <br>**Permissions**: Researcher, Admin
    """

    queryset = Classification.objects.all()
    permission_classes = [IsResearcherOrReadOnly | IsAdminUser]
    serializer_class = ClassificationSerializer
