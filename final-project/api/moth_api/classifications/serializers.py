from rest_framework import serializers

from classifications.models import Classification
from classifications.services import update_classification
from constants import DEFAULT_SPECIES
from images.models import Image
from jobs.models import Job


class ClassificationSerializer(serializers.ModelSerializer):

    image = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name='image-detail',
    )
    file = serializers.SerializerMethodField()

    class Meta:
        model = Classification
        fields = [
            'url',
            'species',
            'accuracy',
            'image',
            'file',
            'is_automated',
            'needs_review',
        ]

    def get_file(self, obj):
        request = self.context.get('request')
        file_url = obj.image.file.url
        return request.build_absolute_uri(file_url)

    def update(self, instance, validated_data):
        return update_classification(instance, validated_data)
