from model_bakery import baker

from django.urls import reverse
from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase

from users.models import User
from users.serializers import CustomFCMDeviceSerializer, UserSerializer


class GetAllUsersTest(APITestCase):
    """
    Test module for getting all users
    """

    def setUp(self):
        self.url = reverse('user-list')

    def test_anon_get_all_users(self):
        """
        Ensure that an anonymous user cannot access the list of users
        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_all_users(self):
        """
        Ensure that a normal user cannot access the list of users
        """

        user = baker.make('users.User')
        self.client.force_authenticate(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_all_users(self):
        """
        Ensure that an admin can access the list of users
        """

        request = APIRequestFactory().get(self.url)
        serializer = UserSerializer(
            User.objects.all(), many=True, context={'request': Request(request)}
        )

        admin = baker.make('users.User', is_staff=True)
        self.client.force_authenticate(admin)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)


class GetSingleUserTest(APITestCase):
    """
    Test module for getting a single user
    """

    def setUp(self):
        self.user = baker.make('users.User')
        self.user_url = reverse('user-detail', kwargs={'uid': self.user.uid})

        self.admin = baker.make('users.User', is_staff=True)
        self.admin_url = reverse('user-detail', kwargs={'uid': self.admin.uid})

    def test_anon_get_user(self):
        """
        Ensure that an anonymous user cannot access the profile of a user
        """

        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_user(self):
        """
        Ensure that the specified user can access his or her profile
        """

        request = APIRequestFactory().get(self.user_url)
        serializer = UserSerializer(self.user, context={'request': Request(request)})

        self.client.force_authenticate(self.user)
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_get_diff_user(self):
        """
        Ensure that a user cannot access someone else's profile
        """

        self.client.force_authenticate(self.user)
        response = self.client.get(self.admin_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_user(self):
        """
        Ensure that an admin can access someone else's profile
        """

        request = APIRequestFactory().get(self.user_url)
        serializer = UserSerializer(self.user, context={'request': Request(request)})

        self.client.force_authenticate(self.admin)
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class UpdateSingleUserTest(APITestCase):
    """
    Test module for updating a single user
    """

    def setUp(self):
        self.user = baker.make('users.User')
        self.user_url = reverse('user-detail', kwargs={'uid': self.user.uid})

        self.admin = baker.make('users.User', is_staff=True)
        self.admin_url = reverse('user-detail', kwargs={'uid': self.admin.uid})

    def test_anon_update_user(self):
        """
        Ensure that an anonymous user cannot update the profile of a user
        """

        response = self.client.put(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_invalid_update_user(self):
        """
        Ensure that the specified user cannot update his or her own profile with invalid data
        """

        invalid_payload = {
            'uid': 'invalid_uid',
        }

        self.client.force_authenticate(self.user)
        response = self.client.put(self.user_url, data=invalid_payload)
        self.user.refresh_from_db()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Invalid update silently fails
        self.assertNotEqual(self.user.uid, invalid_payload.get('uid'))

    def test_user_valid_update_user(self):
        """
        Ensure that the specified user can update his or her own profile with valid data
        """

        valid_payload = {
            'first_name': 'Tester',
            'last_name': 'McTest',
        }

        self.client.force_authenticate(self.user)
        response = self.client.put(self.user_url, data=valid_payload)
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, valid_payload.get('first_name'))
        self.assertEqual(self.user.last_name, valid_payload.get('last_name'))

    def test_user_update_diff_user(self):
        """
        Ensure that the specified user cannot update someone else's profile
        """

        self.client.force_authenticate(self.user)
        response = self.client.put(self.admin_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_update_user(self):
        """
        Ensure that an admin can update someone else's profile
        """

        valid_payload = {
            'first_name': 'Tester',
            'last_name': 'McTest',
        }

        self.client.force_authenticate(self.admin)
        response = self.client.put(self.user_url, data=valid_payload)
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, valid_payload.get('first_name'))
        self.assertEqual(self.user.last_name, valid_payload.get('last_name'))


class DeleteSingleUserTest(APITestCase):
    """
    Test module for deleting a single user
    """

    def setUp(self):
        self.user = baker.make('users.User')
        self.user_url = reverse('user-detail', kwargs={'uid': self.user.uid})

        self.admin = baker.make('users.User', is_staff=True)
        self.admin_url = reverse('user-detail', kwargs={'uid': self.admin.uid})

    def test_anon_delete_user(self):
        """
        Ensure that an anonymous user cannot delete someone else's profile
        """

        response = self.client.delete(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_user(self):
        """
        Ensure that a user cannot delete their own account
        """

        self.client.force_authenticate(self.user)
        response = self.client.delete(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_diff_user(self):
        """
        Ensure that a user cannot delete someone else's account
        """

        self.client.force_authenticate(self.user)
        response = self.client.delete(self.admin_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_delete_user(self):
        """
        Ensure that an admin can delete someone else's account
        """

        self.client.force_authenticate(self.admin)
        response = self.client.delete(self.user_url)
        self.user.refresh_from_db()

        self.assertEqual(response.data, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.user.is_active)


class GetDevicesByUserTest(APITestCase):
    """
    Test module for getting all devices by a specific user
    """

    def setUp(self):
        self.user = baker.make('users.User')
        self.user_device = baker.make('fcm_django.FCMDevice', user=self.user)
        self.user_url = reverse('fcmdevice-user-list', kwargs={'uid': self.user.uid})

        self.admin = baker.make('users.User', is_staff=True)
        self.admin_device = baker.make('fcm_django.FCMDevice', user=self.admin)
        self.admin_url = reverse('fcmdevice-user-list', kwargs={'uid': self.admin.uid})

    def test_anon_get_devices(self):
        """
        Ensure that an anonymous user cannot access the list of devices of a user
        """

        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_devices(self):
        """
        Ensure that a user can access his or her list of images
        """

        request = APIRequestFactory().get(self.user_url)
        serializer = CustomFCMDeviceSerializer(
            FCMDevice.objects.filter(user=self.user),
            many=True,
            context={'request': Request(request)},
        )

        self.client.force_authenticate(self.user)
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_user_get_diff_user_devices(self):
        """
        Ensure that a user cannot access someone else's list of devices
        """

        self.client.force_authenticate(self.user)
        response = self.client.get(self.admin_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_user_devices(self):
        """
        Ensure that an admin can access someone else's list of devices
        """

        request = APIRequestFactory().get(self.user_url)
        serializer = CustomFCMDeviceSerializer(
            FCMDevice.objects.filter(user=self.user),
            many=True,
            context={'request': Request(request)},
        )

        self.client.force_authenticate(self.admin)
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)


class CreateNewDeviceTest(APITestCase):
    """
    Test module for adding a device to the API
    """

    def setUp(self):
        self.user = baker.make('users.User')
        self.user_url = reverse('fcmdevice-user-list', kwargs={'uid': self.user.uid})

        self.admin = baker.make('users.User', is_staff=True)
        self.admin_url = reverse('fcmdevice-user-list', kwargs={'uid': self.admin.uid})

        self.valid_payload = {
            'registration_id': 'abcd1234',
            'type': 'ios',
        }

        self.invalid_payload = {
            'registration_id': 'abcd1234',
            'type': 'phone',
        }

    def test_anon_create_device(self):
        """
        Ensure that an anonymous user cannot add a device under a user's profile
        """

        response = self.client.post(self.user_url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_invalid_create_device(self):
        """
        Ensure that the specified user cannot add a device with invalid data
        """

        self.client.force_authenticate(self.user)
        response = self.client.post(self.user_url, data=self.invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_valid_create_device(self):
        """
        Ensure that the specified user can add a device with valid data
        """

        self.client.force_authenticate(self.user)
        response = self.client.post(self.user_url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_create_device_diff_user(self):
        """
        Ensure that a user/admin cannot add a device to another user's profile
        """

        self.client.force_authenticate(self.admin)
        response = self.client.post(self.user_url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetSingleDeviceTest(APITestCase):
    """
    Test module for getting a single device
    """

    def setUp(self):
        self.user = baker.make('users.User')
        self.user_device = baker.make('fcm_django.FCMDevice', user=self.user)
        self.user_device_url = reverse(
            'fcmdevice-detail', kwargs={'pk': self.user_device.id}
        )

        self.admin = baker.make('users.User', is_staff=True)
        self.admin_device = baker.make('fcm_django.FCMDevice', user=self.admin)
        self.admin_device_url = reverse(
            'fcmdevice-detail', kwargs={'pk': self.admin_device.id}
        )

    def test_anon_get_device(self):
        """
        Ensure that an anonymous user cannot access the device information of a user
        """

        response = self.client.get(self.user_device_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_device(self):
        """
        Ensure that the specified user can access his or her device information
        """

        request = APIRequestFactory().get(self.user_device_url)
        serializer = CustomFCMDeviceSerializer(
            self.user_device, context={'request': Request(request)}
        )

        self.client.force_authenticate(self.user)
        response = self.client.get(self.user_device_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_get_diff_user_device(self):
        """
        Ensure that a user cannot access someone else's device information
        """

        self.client.force_authenticate(self.user)
        response = self.client.get(self.admin_device_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_user_device(self):
        """
        Ensure that an admin can access someone else's device information
        """

        request = APIRequestFactory().get(self.user_device_url)
        serializer = CustomFCMDeviceSerializer(
            self.user_device, context={'request': Request(request)}
        )

        self.client.force_authenticate(self.admin)
        response = self.client.get(self.user_device_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
