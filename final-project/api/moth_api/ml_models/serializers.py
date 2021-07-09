from rest_framework import serializers

from ml_models.models import MLModel


class MLModelSerializer(serializers.ModelSerializer):

    date_created = serializers.DateTimeField(format='%m/%d/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = MLModel
        fields = [
            'id',
            'url',
            'name',
            'file_name',
            'date_created',
            'model_type',
            'rating',
            'comments',
        ]


class MLModelUpdateSerializer(MLModelSerializer):
    class Meta:
        model = MLModel
        fields = [
            'id',
            'url',
            'name',
            'file_name',
            'date_created',
            'model_type',
            'rating',
            'comments',
        ]
        read_only_fields = [
            'name',
            'model_type',
            'file_name',
        ]
