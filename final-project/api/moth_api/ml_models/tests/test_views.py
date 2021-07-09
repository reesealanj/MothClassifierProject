from model_bakery import baker
import os

from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase

from ml_models.models import MLModel
from ml_models.serializers import MLModelSerializer


class GetAllMLModelsTest(APITestCase):
    """
    Test module for getting all ML models
    """

    def setUp(self):
        self.url = reverse('mlmodel-list')
        baker.make('ml_models.MLModel')

    def test_anon_get_all_ml_models(self):
        """
        Ensure that anonymous users cannot access the list of models
        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_all_ml_models(self):
        """
        Ensure that users cannot access the list of models
        """

        user = baker.make('users.User')
        self.client.force_authenticate(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_all_ml_models(self):
        """
        Ensure that admins can access the list of models
        """

        request = APIRequestFactory().get(self.url)
        serializer = MLModelSerializer(
            MLModel.objects.all(), many=True, context={'request': Request(request)}
        )

        admin = baker.make('users.User', is_staff=True)
        self.client.force_authenticate(admin)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)


class CreateNewMLModelTest(APITestCase):
    """
    Test module for creating a new ML Model
    """

    def setUp(self):
        self.admin = baker.make('users.User', is_staff=True)
        self.url = reverse('mlmodel-list')

        self.valid_payload = {
            'name': 'Test Model',
            'file_name': 'test.h5',
            'model_type': 'classifier',
        }

    def test_anon_create_ml_model(self):
        """
        Ensure that an anonymous user cannot add a ML model
        """

        response = self.client.post(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_create_ml_model(self):
        """
        Ensure that a regular user cannot add a ML model
        """

        user = baker.make('users.User')
        self.client.force_authenticate(user)
        response = self.client.post(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_invalid_create_ml_model(self):
        """
        Ensure that an admin cannot create an invalid model
        """

        self.client.force_authenticate(self.admin)
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_valid_create_ml_model(self):
        """
        Ensure that an admin can create a valid model
        """

        self.client.force_authenticate(self.admin)
        response = self.client.post(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetMLModelsByJobTest(APITestCase):
    """
    Test module for getting all ML models by a specific job
    """

    def setUp(self):
        self.image = baker.make('images.Image', _create_files=True)
        model = baker.make('ml_models.MLModel')

        self.job = baker.make('jobs.Job', models=[model], image=self.image)
        self.url = reverse('mlmodel-job-list', kwargs={'pk': self.job.id})

    def tearDown(self):
        os.remove(self.image.file.path)

    def test_anon_get_ml_models(self):
        """
        Ensure that an anonymous user cannot access the list of ML models of a job
        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_ml_models(self):
        """
        Ensure that a regular user cannot access the list of ML models of a job
        """

        user = baker.make('users.User')
        self.client.force_authenticate(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_ml_models(self):
        """
        Ensure that an admin can access the list of ML models of a job
        """

        request = APIRequestFactory().get(self.url)
        serializer = MLModelSerializer(
            self.job.models.all(), many=True, context={'request': Request(request)}
        )

        admin = baker.make('users.User', is_staff=True)
        self.client.force_authenticate(admin)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)


class GetSingleMLModelTest(APITestCase):
    """
    Test module for getting a single ML model
    """

    def setUp(self):
        self.model = baker.make('ml_models.MLModel')
        self.url = reverse('mlmodel-detail', kwargs={'pk': self.model.id})

    def test_anon_get_ml_model(self):
        """
        Ensure that an anonymous user cannot access a ML model
        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_ml_model(self):
        """
        Ensure that a regular user cannot access a ML model
        """

        user = baker.make('users.User')
        self.client.force_authenticate(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_ml_model(self):
        """
        Ensure that an admin can access a ML model
        """

        request = APIRequestFactory().get(self.url)
        serializer = MLModelSerializer(
            self.model, context={'request': Request(request)}
        )

        admin = baker.make('users.User', is_staff=True)
        self.client.force_authenticate(admin)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class UpdateSingleMLModelTest(APITestCase):
    """
    Test module for updating a single ML model
    """

    def setUp(self):
        self.model = baker.make('ml_models.MLModel')
        self.url = reverse('mlmodel-detail', kwargs={'pk': self.model.id})

        self.valid_payload = {
            'rating': 100,
        }

    def test_anon_update_ml_model(self):
        """
        Ensure that an anonymous user cannot update a ML model
        """

        response = self.client.put(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_ml_model(self):
        """
        Ensure that a regular user cannot update a ML model
        """

        user = baker.make('users.User')
        self.client.force_authenticate(user)
        response = self.client.put(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_invalid_update_ml_model(self):
        """
        Ensure that an admin cannot update a ML model with invalid data
        """

        invalid_payload = {
            'rating': 'invalid rating',
        }

        admin = baker.make('users.User', is_staff=True)
        self.client.force_authenticate(admin)
        response = self.client.put(self.url, data=invalid_payload)
        self.model.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.model.rating, invalid_payload.get('rating'))

    def test_admin_valid_update_ml_model(self):
        """
        Ensure that an admin can update a ML model with valid data
        """

        admin = baker.make('users.User', is_staff=True)
        self.client.force_authenticate(admin)
        response = self.client.put(self.url, data=self.valid_payload)
        self.model.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.model.rating, self.valid_payload.get('rating'))
