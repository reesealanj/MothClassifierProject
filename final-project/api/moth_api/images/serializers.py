import imagehash
import PIL

from rest_framework import serializers

from images.models import Image
from users.models import User


class ImageSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name='user-detail', lookup_field='uid',
    )
    date_taken = serializers.DateTimeField(format='%m/%d/%Y %H:%M:%S', read_only=True)
    hash = serializers.ReadOnlyField()
    jobs = serializers.HyperlinkedIdentityField(view_name='job-image-list')
    classification = serializers.HyperlinkedIdentityField(
        view_name='classification-detail'
    )

    class Meta:
        model = Image
        fields = [
            'id',
            'url',
            'user',
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
            'is_training',
            'hash',
            'jobs',
            'classification',
        ]

    def create(self, validated_data):
        validated_data['user_id'] = self.context['user_id']
        return super(ImageSerializer, self).create(validated_data)

    def validate_file(self, file):
        # Check the hash of the file to see if it is a duplicate
        # Duplicates only apply to the same user
        hash = str(imagehash.phash(PIL.Image.open(file)))
        if Image.objects.filter(hash=hash, user_id=self.context['user_id']).exists():
            raise serializers.ValidationError('Image already exists')

        return file
