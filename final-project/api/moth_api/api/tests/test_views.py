from rest_framework import status
from rest_framework.test import APITestCase


class GetAPIRoot(APITestCase):
    """
    Test module for the API root
    """

    def setUp(self):
        self.url = '/api/v1/'

    def test_get_api_root(self):
        """
        Ensure that anyone can access the API root
        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(
            response.data, ['users', 'images', 'jobs', 'classifications', 'models']
        )
