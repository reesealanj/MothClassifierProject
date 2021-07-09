from model_bakery import baker
import PIL
import tempfile
import os

from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase

from images.models import Image
from images.serializers import ImageSerializer


class GetAllImagesTest(APITestCase):
    """
    Test module for getting all images
    """

    def setUp(self):
        self.image = baker.make('images.Image', _create_files=True)

    def tearDown(self):
        os.remove(self.image.file.path)

    def test_get_all_images(self):
        """
        Ensure that anyone can access the list of images
        """

        url = reverse('image-list')
        response = self.client.get(url)

        request = APIRequestFactory().get(url)
        serializer = ImageSerializer(
            Image.objects.all(), many=True, context={'request': Request(request)}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_all_images_download(self):
        """
        Ensure that anyone can download the list of images
        """

        url = reverse('image-list-download')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.get('Content-Disposition'), 'attachment; filename="dataset.zip"'
        )


class GetImagesByUserTest(APITestCase):
    """
    Test module for getting all images by a specific user
    """

    def setUp(self):
        self.user = baker.make('users.User')
        self.user_url = reverse('image-user-list', kwargs={'uid': self.user.uid})
        self.image = baker.make('images.Image', user=self.user, _create_files=True)

        self.admin = baker.make('users.User', is_staff=True)
        self.admin_url = reverse('image-user-list', kwargs={'uid': self.admin.uid})

    def tearDown(self):
        os.remove(self.image.file.path)

    def test_anon_get_images(self):
        """
        Ensure that an anonymous user cannot access the list of images of a user
        """

        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_images(self):
        """
        Ensure that a user can access his or her list of images
        """

        request = APIRequestFactory().get(self.user_url)
        serializer = ImageSerializer(
            Image.objects.filter(user=self.user),
            many=True,
            context={'request': Request(request)},
        )

        self.client.force_authenticate(self.user)
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_user_get_diff_user_images(self):
        """
        Ensure that a user cannot access someone else's list of images
        """

        self.client.force_authenticate(self.user)
        response = self.client.get(self.admin_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_user_images(self):
        """
        Ensure that an admin can access someone else's list of images
        """

        request = APIRequestFactory().get(self.user_url)
        serializer = ImageSerializer(
            Image.objects.filter(user=self.user),
            many=True,
            context={'request': Request(request)},
        )

        self.client.force_authenticate(self.admin)
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)


class CreateNewImageTest(APITestCase):
    """
    Test module for uploading an image to the API
    """

    def setUp(self):
        self.user = baker.make('users.User')
        self.user_url = reverse('image-user-list', kwargs={'uid': self.user.uid})

        self.admin = baker.make('users.User', is_staff=True)
        self.admin_url = reverse('image-user-list', kwargs={'uid': self.admin.uid})

        image = PIL.Image.new('RGB', size=(1, 1))
        self.temp = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(self.temp)

        self.file = open(self.temp.name, 'rb')
        self.valid_payload = {'file': self.file}

        self.invalid_payload = {'file': tempfile.NamedTemporaryFile(suffix='.txt')}

    def tearDown(self):
        self.file.close()

        for image in Image.objects.all():
            os.remove(image.file.path)
            image.delete()

    def test_anon_create_image(self):
        """
        Ensure that an anonymous user cannot upload an image under a user's profile
        """

        response = self.client.post(self.user_url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_invalid_create_image(self):
        """
        Ensure that the specified user cannot add an image with invalid data
        """

        self.client.force_authenticate(self.user)
        response = self.client.post(self.user_url, data=self.invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_valid_create_image(self):
        """
        Ensure that the specified user can add an image with valid data
        """

        self.client.force_authenticate(self.user)
        response = self.client.post(self.user_url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_create_image_diff_user(self):
        """
        Ensure that a user cannot add an image to another user's profile
        """

        self.client.force_authenticate(self.user)
        response = self.client.post(self.admin_url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_image(self):
        """
        Ensure that an admin can add an image under someone's name
        """

        self.client.force_authenticate(self.admin)
        response = self.client.post(self.user_url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetSingleImageTest(APITestCase):
    """
    Test module for getting a single image
    """

    def setUp(self):
        self.image = baker.make('images.Image', _create_files=True)
        self.image_url = reverse('image-detail', kwargs={'pk': self.image.id})

    def tearDown(self):
        os.remove(self.image.file.path)

    def test_get_image(self):
        """
        Ensure that anyone can access a single image
        """

        request = APIRequestFactory().get(self.image_url)
        serializer = ImageSerializer(self.image, context={'request': Request(request)})

        response = self.client.get(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class DeleteSingleImageTest(APITestCase):
    """
    Test module for deleting a single image
    """

    def setUp(self):
        self.user = baker.make('users.User')
        self.admin = baker.make('users.User', is_staff=True)

        self.image = baker.make('images.Image', _create_files=True, user=self.user)
        self.image_url = reverse('image-detail', kwargs={'pk': self.image.id})

    def tearDown(self):
        try:
            os.remove(self.image.file.path)
        except FileNotFoundError:
            pass

    def test_anon_delete_user(self):
        """
        Ensure that a user cannot delete an image
        """

        response = self.client.delete(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_image(self):
        """
        Ensure that a user can delete his/her own image
        """

        self.client.force_authenticate(self.user)
        response = self.client.delete(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(os.path.exists(self.image.file.path))

    def test_user_delete_image_diff_user(self):
        """
        Ensure that a user cannot delete someone else's image
        """

        self.image.user = self.admin
        self.image.save()

        self.client.force_authenticate(self.user)
        response = self.client.delete(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_delete_image(self):
        """
        Ensure that an admin can delete someone else's image
        """

        self.client.force_authenticate(self.admin)
        response = self.client.delete(self.image_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
