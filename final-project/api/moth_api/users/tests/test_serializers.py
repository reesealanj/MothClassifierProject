from model_bakery import baker

from rest_framework.test import APITestCase

from users.serializers import UserSerializer


class TestUserSerializer(APITestCase):
    """
    Test module for UserSerializer
    """

    def setUp(self):
        self.serializer = UserSerializer()

    def test_create_unusable_password(self):
        """
        Ensure that the create() method of the UserSerializer creates an unusable password
        """

        user_data = baker.prepare('users.User')
        valid_data = {'email': user_data.email, 'uid': user_data.uid}

        user = self.serializer.create(valid_data)
        self.assertFalse(user.has_usable_password())
