from model_bakery import baker
import os
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase

from jobs.models import Job
from jobs.serializers import JobSerializer


class GetAllJobsTest(APITestCase):
    """
    Test module for getting all jobs
    """

    def setUp(self):
        self.url = reverse('job-list')

    def test_anon_get_all_jobs(self):
        """
        Ensure that an anonymous user cannot access the list of jobs
        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_all_jobs(self):
        """
        Ensure that a normal user cannot access the list of jobs
        """

        user = baker.make('users.User')
        self.client.force_authenticate(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_all_jobs(self):
        """
        Ensure that an admin can access the list of jobs
        """

        request = APIRequestFactory().get(self.url)
        serializer = JobSerializer(
            Job.objects.all(), many=True, context={'request': Request(request)}
        )

        admin = baker.make('users.User', is_staff=True)
        self.client.force_authenticate(admin)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)


class GetJobsByImageTest(APITestCase):
    """
    Test module for getting all jobs for a specific image
    """

    def setUp(self):
        self.user = baker.make('users.User')
        self.image = baker.make(
            'images.Image', user_id=self.user.id, _create_files=True
        )
        self.image_url = reverse('job-image-list', kwargs={'pk': self.image.id})
        baker.make('jobs.Job', image_id=self.image.id)

        self.admin = baker.make('users.User', is_staff=True)

    def tearDown(self):
        os.remove(self.image.file.path)

    def test_anon_get_jobs(self):
        """
        Ensure that an anonymous user cannot access the list of jobs by image
        """

        response = self.client.get(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_jobs(self):
        """
        Ensure that a user can access his or her jobs for his or her image
        """

        request = APIRequestFactory().get(self.image_url)
        serializer = JobSerializer(
            Job.objects.filter(image_id=self.image.id),
            many=True,
            context={'request': Request(request)},
        )

        self.client.force_authenticate(self.user)
        response = self.client.get(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_user_get_diff_user_jobs(self):
        """
        Ensure that a user cannot access the jobs for someone else's image
        """

        self.image.user_id = self.admin.id
        self.image.save()

        self.client.force_authenticate(self.user)
        response = self.client.get(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_user_jobs(self):
        """
        Ensure that an admin can access someone else's jobs
        """

        request = APIRequestFactory().get(self.image_url)
        serializer = JobSerializer(
            Job.objects.filter(image_id=self.image.id),
            many=True,
            context={'request': Request(request)},
        )

        self.client.force_authenticate(self.user)
        response = self.client.get(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)


class CreateNewJobTest(APITestCase):
    """
    Test module for submitting a job to the API
    """

    def setUp(self):
        self.user = baker.make('users.User')
        self.image = baker.make(
            'images.Image', user_id=self.user.id, _create_files=True
        )
        self.image_url = reverse('job-image-list', kwargs={'pk': self.image.id})

        self.admin = baker.make('users.User', is_staff=True)

    def tearDown(self):
        os.remove(self.image.file.path)

    @patch('jobs.views.handle_job.delay')
    def test_anon_create_job(self, mock_handle_job):
        """
        Ensure that an anonymous user cannot create a job
        """

        response = self.client.post(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('jobs.views.handle_job.delay')
    def test_user_invalid_create_job(self, mock_handle_job):
        """
        Ensure that a user cannot create a job for his or her own image with invalid data
        """

        self.client.force_authenticate(self.user)
        response = self.client.post(self.image_url, data={'job_type': 'invalid_job'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('jobs.views.handle_job.delay')
    def test_user_valid_create_job(self, mock_handle_job):
        """
        Ensure that a user can create a job for his or her image with valid data
        """

        self.client.force_authenticate(self.user)
        response = self.client.post(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_handle_job.assert_called()

    @patch('jobs.views.handle_job.delay')
    def test_user_create_job_diff_user(self, mock_handle_job):
        """
        Ensure that a user cannot create a job for someone else's image
        """

        self.image.user_id = self.admin.id
        self.image.save()

        self.client.force_authenticate(self.user)
        response = self.client.post(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('jobs.views.handle_job.delay')
    def test_admin_create_job(self, mock_handle_job):
        """
        Ensure that an admin can create a job for someone else's image
        """

        self.client.force_authenticate(self.admin)
        response = self.client.post(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_handle_job.assert_called()


class GetSingleJobTest(APITestCase):
    """
    Test module for getting a single job
    """

    def setUp(self):
        self.user = baker.make('users.User')
        self.image = baker.make(
            'images.Image', user_id=self.user.id, _create_files=True
        )
        self.job = baker.make('jobs.Job', image_id=self.image.id)
        self.url = reverse('job-detail', kwargs={'pk': self.job.id})

        self.admin = baker.make('users.User', is_staff=True)

    def tearDown(self):
        os.remove(self.image.file.path)

    def test_anon_get_job(self):
        """
        Ensure that an anonymous user cannot get a job
        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_job(self):
        """
        Ensure that a user can view their own job
        """

        request = APIRequestFactory().get(self.url)
        serializer = JobSerializer(self.job, context={'request': Request(request)})

        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_get_job_diff_user(self):
        """
        Ensure that a user cannot view someone else's job
        """

        self.job.image.user_id = self.admin.id
        self.job.image.save()

        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_job(self):
        """
        Ensure that an admin can view someone else's job
        """

        request = APIRequestFactory().get(self.url)
        serializer = JobSerializer(self.job, context={'request': Request(request)})

        self.client.force_authenticate(self.admin)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
