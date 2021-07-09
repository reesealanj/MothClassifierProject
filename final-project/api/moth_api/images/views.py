import os

from django.conf import settings
from django.http import FileResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser

from classifications.models import Classification
from constants import TRAINING_FILE
from images.models import Image
from images.schemas import ZipAutoSchema
from images.permissions import IsOwnerOfImage
from images.serializers import ImageSerializer
from images.services import download_images
from users.models import User
from users.permissions import IsSelf


class ImageList(generics.ListAPIView):
    """
    General View Description

    get: Returns a list of images in the system
        <br>**Permissions**: Public
    """

    queryset = Image.objects.order_by('-id')
    serializer_class = ImageSerializer
    filterset_fields = [
        'country',
        'region',
        'county',
        'city',
        'zip_code',
        'street',
        'lat',
        'lng',
        'date_taken',
        'width',
        'height',
        'is_training',
    ]
    ordering_fields = [
        'id',
        'file',
        'country',
        'region',
        'county',
        'city',
        'zip_code',
        'street',
        'lat',
        'lng',
        'date_taken',
        'width',
        'height',
    ]


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        auto_schema=ZipAutoSchema,
        responses={
            '200': openapi.Response(
                'File Attachment', schema=openapi.Schema(type=openapi.TYPE_FILE)
            ),
        },
        produces='application/zip',
    ),
)
class ImageListDownload(ImageList):
    """
    General View Description

    get: Downloads images in the system
        <br>**Permissions**: Public
    """

    serializer_class = None
    pagination_class = None
    ordering_fields = []

    def get(self, request, *args, **kwargs):
        file_name, metadata_name = download_images(
            request, self.filter_queryset(self.get_queryset())
        )

        # Return the zip file and clean up
        response = FileResponse(
            open(file_name, 'rb'), content_type='application/zip', as_attachment=True
        )

        if file_name != TRAINING_FILE:
            os.remove(file_name)
        try:
            os.remove(metadata_name)
        except TypeError:
            pass  # Ignore if metadata_name is None

        return response


class ImageListByUser(ImageList, generics.ListCreateAPIView):
    """
    General View Description

    get: Returns images associated with the specified user
        <br>**Permissions**: Specified User, Admin
        
    post: Adds an image and a blank classification to the system and associates it with the specified user
        <br>**Permissions**: Specified User, Admin
    """

    lookup_field = 'uid'
    permission_classes = [IsSelf | IsAdminUser]
    parser_classes = (FormParser, MultiPartParser)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return Image.objects.none()

        user = User.objects.get(uid=self.kwargs.get('uid'))
        return Image.objects.filter(user=user).order_by('-id')

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        # Create a blank classification when an image is created
        Classification.objects.create(
            image_id=response.data.get('id'), needs_review=True
        )
        return response

    # Override this function to extract the user id from the url
    def get_serializer_context(self):
        context = super(ImageListByUser, self).get_serializer_context()

        if getattr(self, 'swagger_fake_view', False):
            # context just for schema generation metadata
            return context

        user = User.objects.get(uid=self.kwargs.get('uid'))
        context.update({'user_id': user.id})

        return context


class ImageDetail(generics.RetrieveDestroyAPIView):
    """
    General View Description

    get: Returns an image with the specified id
        <br>**Permissions**: Public

    delete: Deletes the specified image from the system
        <br>**Permissions**: Owner of Image, Admin
    """

    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def delete(self, request, *args, **kwargs):
        # Delete the image from the web server
        path = self.get_object().file.path
        os.remove(path)
        try:
            os.rmdir(os.path.dirname(path))
        except OSError:
            pass

        return self.destroy(request, *args, **kwargs)

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'DELETE':
            permission_classes = [IsOwnerOfImage | IsAdminUser]

        return [permission() for permission in permission_classes]
