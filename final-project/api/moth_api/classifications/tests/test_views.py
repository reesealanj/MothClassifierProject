from model_bakery import baker
import os

from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase

from classifications.models import Classification
from classifications.serializers import ClassificationSerializer


class GetAllClassificationsTest(APITestCase):
    """
    Test module for getting all classifications
    """

    def setUp(self):
        self.url = reverse('classification-list')
        self.image = baker.make('images.Image', _create_files=True)
        baker.make('classifications.Classification', image=self.image)

    def tearDown(self):
        os.remove(self.image.file.path)

    def test_get_all_images(self):
        """
        Ensure that anyone can access the list of images
        """

        request = APIRequestFactory().get(self.url)
        serializer = ClassificationSerializer(
            Classification.objects.all(),
            many=True,
            context={'request': Request(request)},
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)


class GetSingleClassificationTest(APITestCase):
    """
    Test module for getting a single classification
    """

    def setUp(self):
        self.image = baker.make('images.Image', _create_files=True)
        self.classification = baker.make(
            'classifications.Classification', image=self.image
        )
        self.url = reverse('classification-detail', kwargs={'pk': self.image.id})

    def tearDown(self):
        os.remove(self.image.file.path)

    def test_get_classification(self):
        """
        Ensure that anyone can access a classification
        """

        request = APIRequestFactory().get(self.url)
        serializer = ClassificationSerializer(
            self.classification, context={'request': Request(request)}
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class UpdateSingleClassificationTest(APITestCase):
    """
    Test module for updating a single classification
    """

    def setUp(self):
        self.image = baker.make('images.Image', _create_files=True)
        self.classification = baker.make(
            'classifications.Classification', image=self.image
        )
        self.url = reverse('classification-detail', kwargs={'pk': self.image.id})

        self.user = baker.make('users.User')

        self.valid_payload = {
            'species': 'Test Species',
        }

        self.invalid_payload = {
            'accuracy': 'invalid',
        }

    def tearDown(self):
        self.image.refresh_from_db()
        os.remove(self.image.file.path)
        try:
            os.rmdir(os.path.dirname(self.image.file.path))
        except OSError:
            pass

    def test_anon_update_classification(self):
        """
        Ensure that an anonymous user cannot update a classification
        """

        response = self.client.put(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_classification(self):
        """
        Ensure that a regular user cannot update a classification
        """

        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_researcher_invalid_update_classification(self):
        """
        Ensure that a researcher cannot update a classification with invalid data
        """

        self.user.is_researcher = True
        self.user.save()

        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data=self.invalid_payload)
        self.classification.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(
            self.classification.accuracy, self.invalid_payload.get('accuracy')
        )

    def test_researcher_valid_update_classification(self):
        """
        Ensure that a researcher can update a classification with valid data
        """

        self.user.is_researcher = True
        self.user.save()

        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data=self.valid_payload)
        self.classification.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.classification.species, self.valid_payload.get('species'))

    def test_admin_update_classification(self):
        """
        Ensure that an admin can update a classification with valid data
        """

        self.user.is_staff = True
        self.user.save()

        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data=self.valid_payload)
        self.classification.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.classification.species, self.valid_payload.get('species'))
