# Authentication backend for handling Firebase Authentication.
from django.utils import timezone
from drf_firebase_auth.authentication import FirebaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class CustomFirebaseAuthentication(FirebaseAuthentication):
    """
    Overrides some functions provided by FirebaseAuthentication 
    to implement custom behavior
    """

    def get_or_create_local_user(self, firebase_user):
        """
        Attempts to return or create a local User from Firebase user data
        """

        email = (
            firebase_user.email
            if firebase_user.email
            else firebase_user.provider_data[0].email
        )

        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                raise AuthenticationFailed(
                    'User is not registered to the application or inactive'
                )

            user.last_login = timezone.now()
            user.save()

            return user
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email, uid=firebase_user.uid, last_login=timezone.now(),
            )

            return user
