from drf_firebase_auth.models import FirebaseUser
from fcm_django.api.rest_framework import FCMDeviceSerializer
from fcm_django.models import FCMDevice
from rest_framework import serializers

from users.models import User, ResearcherRequest


class UserSerializer(serializers.ModelSerializer):

    images = serializers.HyperlinkedIdentityField(
        view_name='image-user-list', lookup_field='uid'
    )
    date_joined = serializers.DateTimeField(format='%m/%d/%Y %H:%M:%S', read_only=True)
    last_login = serializers.DateTimeField(format='%m/%d/%Y %H:%M:%S', read_only=True)
    devices = serializers.HyperlinkedIdentityField(
        view_name='fcmdevice-user-list', lookup_field='uid',
    )
    researcher_requests = serializers.HyperlinkedIdentityField(
        view_name='researcherrequest-user-list', lookup_field='uid',
    )

    class Meta:
        model = User
        fields = [
            'id',
            'uid',
            'url',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'last_login',
            'is_researcher',
            'is_staff',
            'is_active',
            'images',
            'devices',
            'researcher_requests',
        ]
        read_only_fields = [
            'uid',
            'email',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'uid'},
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_unusable_password()
        user.save()

        return user


class CustomFCMDeviceSerializer(FCMDeviceSerializer):
    class Meta(FCMDeviceSerializer.Meta):
        fields = FCMDeviceSerializer.Meta.fields + ('url',)

    def create(self, validated_data):
        validated_data['user_id'] = self.context['user_id']
        return super(CustomFCMDeviceSerializer, self).create(validated_data)


class CustomFCMDeviceUpdateSerializer(CustomFCMDeviceSerializer):
    class Meta(CustomFCMDeviceSerializer.Meta):
        read_only_fields = [
            'device_id',
            'type',
        ]

    def update(self, instance, validated_data):
        validated_data.pop('registration_id')
        return super(CustomFCMDeviceUpdateSerializer, self).update(
            instance, validated_data
        )


class UserResearcherRequestSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name='user-detail', lookup_field='uid',
    )
    request_date = serializers.DateTimeField(format='%m/%d/%Y %H:%M:%S', read_only=True)
    response_date = serializers.DateTimeField(
        format='%m/%d/%Y %H:%M:%S', read_only=True
    )
    status = serializers.ChoiceField(choices=ResearcherRequest.STATUS, read_only=True)

    class Meta:
        model = ResearcherRequest
        fields = [
            'id',
            'url',
            'user',
            'request_date',
            'response_date',
            'status',
            'comments',
        ]
        read_only_fields = [
            'user',
            'request_date',
            'status',
            'comments',
        ]

    def create(self, validated_data):
        validated_data['user_id'] = self.context['user_id']
        return super(UserResearcherRequestSerializer, self).create(validated_data)


class AdminResearcherRequestSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name='user-detail', lookup_field='uid',
    )
    request_date = serializers.DateTimeField(format='%m/%d/%Y %H:%M:%S', read_only=True)
    response_date = serializers.DateTimeField(
        format='%m/%d/%Y %H:%M:%S', read_only=True
    )
    status = serializers.ChoiceField(choices=ResearcherRequest.STATUS)

    class Meta:
        model = ResearcherRequest
        fields = [
            'id',
            'url',
            'user',
            'request_date',
            'response_date',
            'status',
            'comments',
        ]
        read_only_fields = [
            'request_date',
            'response_date',
        ]

    def update(self, instance, validated_data):
        status = validated_data.pop('status')
        if status == 'approved':
            instance.approve()
        elif status == 'denied':
            instance.deny()

        return super(AdminResearcherRequestSerializer, self).update(
            instance, validated_data
        )
