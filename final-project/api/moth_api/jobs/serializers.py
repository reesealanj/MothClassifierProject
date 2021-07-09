from rest_framework import serializers

from images.models import Image
from jobs.models import Job


class JobSerializer(serializers.ModelSerializer):

    image = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name='image-detail'
    )
    date_issued = serializers.DateTimeField(format='%m/%d/%Y %H:%M:%S', read_only=True)
    last_modified = serializers.DateTimeField(
        format='%m/%d/%Y %H:%M:%S', read_only=True
    )
    status = serializers.ChoiceField(choices=Job.STATUS, read_only=True)
    models = serializers.HyperlinkedIdentityField(view_name='mlmodel-job-list')

    class Meta:
        model = Job
        fields = [
            'id',
            'url',
            'job_type',
            'image',
            'date_issued',
            'last_modified',
            'status',
            'status_message',
            'models',
        ]
        read_only_fields = [
            'date_issued',
            'last_modified',
            'status',
            'status_message',
        ]

    # Generic get_FOO_display() method provided by Django
    def get_job_type(self, obj):
        return obj.get_job_type_display()

    def create(self, validated_data):
        validated_data['image_id'] = self.context['image_id']
        return super(JobSerializer, self).create(validated_data)
