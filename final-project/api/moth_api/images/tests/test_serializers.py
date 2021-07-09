from model_bakery import baker
import os

from rest_framework import serializers
from rest_framework.test import APITestCase

from images.serializers import ImageSerializer


class TestImageSerializer(APITestCase):
    """
    Test module for ImageSerializer
    """

    def setUp(self):
        self.serializer = ImageSerializer()
        self.image = baker.make('images.Image', _create_files=True)

    def tearDown(self):
        os.remove(self.image.file.path)

    def test_validate_duplicate_file(self):
        """
        Ensure that a duplicate file raises a validation error
        """

        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate_file(self.image.file)
