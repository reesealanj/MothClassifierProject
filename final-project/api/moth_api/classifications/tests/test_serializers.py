from model_bakery import baker
import os
import shutil

from rest_framework.test import APITestCase
from django.conf import settings

from classifications.serializers import ClassificationSerializer


class TestClassificationSerializer(APITestCase):
    """
    Test module for ClassificationSerializer
    """

    def setUp(self):
        self.serializer = ClassificationSerializer()
        self.image = baker.make('images.Image', _create_files=True)
        self.classification = baker.make(
            'classifications.Classification', image=self.image
        )

        species = 'test_species'
        self.data = {
            'species': species,
        }
        self.new_folder = f'{settings.MEDIA_ROOT}{species}'

    def tearDown(self):
        self.image.refresh_from_db()
        os.remove(self.image.file.path)
        try:
            shutil.rmtree(self.new_folder)
        except OSError:
            pass

    def test_move_new_classification(self):
        """
        Ensure that a classification is moved to the correct directory upon being assigned a classification
        """

        os.mkdir(self.new_folder)
        self.serializer.update(self.classification, self.data)

        self.assertEquals(
            os.path.dirname(self.classification.image.file.path), self.new_folder
        )

    def test_create_new_directory(self):
        """
        Ensure that a new directory is created if a new species is classified
        """

        self.assertFalse(os.path.exists(self.new_folder))

        self.serializer.update(self.classification, self.data)

        self.assertTrue(os.path.exists(self.new_folder))
        self.assertEquals(
            os.path.dirname(self.classification.image.file.path), self.new_folder
        )
