from fcm_django.models import FCMDevice
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from users.models import User, ResearcherRequest
from users.permissions import IsOwnerOfDevice, IsOwnerOfResearcherRequest, IsSelf
from users.serializers import (
    CustomFCMDeviceSerializer,
    CustomFCMDeviceUpdateSerializer,
    UserSerializer,
    UserResearcherRequestSerializer,
    AdminResearcherRequestSerializer,
)


class UserList(generics.ListAPIView):
    """
    General View Description
    
    get: Returns a list of users in the system 
        <br>**Permissions**: Admin

    """

    permission_classes = [IsAdminUser]
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filterset_fields = [
        'email',
        'first_name',
        'last_name',
        'is_researcher',
        'is_staff',
        'is_active',
    ]
    ordering_fields = [
        'first_name',
        'last_name',
        'date_joined',
        'last_login',
    ]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    General View Description
    
    get: Returns a user with the specified uid
        <br>**Permissions**: Specified User, Admin

    put: Updates the information for the specified user
        <br>**Permissions**: Specified User, Admin

    patch: Updates the information for the specified user
        <br>**Permissions**: Specified User, Admin
        
    delete: Deletes the specified user from the system by making them inactive
        <br>**Permissions**: Admin
    """

    lookup_field = 'uid'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        # Make the user inactive
        user.is_active = False
        user.save()

        return Response(status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsSelf | IsAdminUser]

        return [permission() for permission in permission_classes]


class DeviceListByUser(generics.ListCreateAPIView):
    """
    General View Description
    
    get: Returns devices asscoiated with the specified user
        <br>**Permissions**: Specified User, Admin
    
    post: Adds a device to the system and associates it with the specified user
        <br>**Permissions**: Specified User
    """

    lookup_field = 'uid'
    serializer_class = CustomFCMDeviceSerializer
    filterset_fields = [
        'active',
        'type',
    ]
    ordering_fields = [
        'id',
        'name',
        'active',
        'date_created',
        'type',
    ]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # quersey just for schema gewneration metadata
            return FCMDevice.objects.none()

        user = User.objects.get(uid=self.kwargs.get('uid'))
        return FCMDevice.objects.filter(user=user).order_by('-id')

    # Override this function to extract the user id from the url
    def get_serializer_context(self):
        context = super(DeviceListByUser, self).get_serializer_context()

        if getattr(self, 'swagger_fake_view', False):
            # context just for schema generation metadata
            return context

        user = User.objects.get(uid=self.kwargs.get('uid'))
        context.update({'user_id': user.id})

        return context

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsSelf | IsAdminUser]
        else:
            permission_classes = [IsSelf]

        return [permission() for permission in permission_classes]


class DeviceDetail(generics.RetrieveUpdateAPIView):
    """
    General View Description

    get: Returns a device with the specified id
        <br>**Permissions**: Owner of Device, Admin
    """

    permission_classes = [IsOwnerOfDevice | IsAdminUser]
    queryset = FCMDevice.objects.all()
    serializer_class = CustomFCMDeviceUpdateSerializer


class ResearcherRequestList(generics.ListAPIView):
    """
    General View Description

    get: Returns a list of researcher requests in the system
        <br>**Permissions**: Admin
    
    """

    queryset = ResearcherRequest.objects.order_by('-id')
    serializer_class = UserResearcherRequestSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['status']
    ordering_fields = [
        'request_date',
        'response_date',
    ]


class ResearcherRequestListByUser(ResearcherRequestList, generics.ListCreateAPIView):

    """
    General View Description

    get: Returns all researcher requests associated with this user
        <br>**Permissions**: Specified User, Admin

    post: (If specified user) Submits a researcher request associated with this user if the user is not already a researcher
        <br>**Permissions**: Specified User, Admin
    """

    lookup_field = 'uid'
    permission_classes = [IsSelf | IsAdminUser]
    serializer_class = UserResearcherRequestSerializer

    def get_queryset(self):
        user = User.objects.get(uid=self.kwargs.get('uid'))
        return ResearcherRequest.objects.filter(user=user).order_by('-id')

    def post(self, request, *args, **kwargs):
        user = User.objects.get(uid=self.kwargs.get('uid'))
        if user.is_researcher:  # Do not let a researcher submit a researcher request
            return Response(status.HTTP_409_CONFLICT)

        return self.create(request, *args, **kwargs)

    # Override this function to extract the user id from the url
    def get_serializer_context(self):
        context = super(ResearcherRequestListByUser, self).get_serializer_context()

        if getattr(self, 'swagger_fake_view', False):
            # context just for schema generation metadata
            return context

        user = User.objects.get(uid=self.kwargs.get('uid'))
        context.update({'user_id': user.id})

        return context


class ResearcherRequestDetail(generics.RetrieveUpdateAPIView):
    """
    General View Description

    get: Returns a researcher request with the specified id
        <br>**Permissions**: Owner of Request, Admin
    
    put: Updates the researcher request with the specified id
        <br>**Permissions**: Admin

    patch: Updates the researcher request with the specified id
        <br>**Permissions**: Admin
    """

    queryset = ResearcherRequest.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsOwnerOfResearcherRequest | IsAdminUser]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminResearcherRequestSerializer

        return UserResearcherRequestSerializer
