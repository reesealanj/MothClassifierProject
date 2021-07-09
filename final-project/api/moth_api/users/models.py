from django.db import models, transaction
from django_fsm import FSMField, transition
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from model_utils import Choices


class CustomUserManager(BaseUserManager):
    """
    Custom user manager to use the email as the username field
    """

    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_unusable_password()
        user.save()

        return user


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True)
    uid = models.CharField(max_length=191, null=False, blank=False, unique=True)
    is_researcher = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class ResearcherRequest(models.Model):

    STATUS = Choices(
        ('pending', 'pending', 'PENDING'),
        ('approved', 'approved', 'APPROVED'),
        ('denied', 'denied', 'DENIED'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    response_date = models.DateTimeField(null=True, blank=True)
    status = FSMField(default=STATUS.pending, choices=STATUS, protected=True)
    comments = models.TextField(blank=True)

    # Implement the FSM for status
    @transition(field=status, source=STATUS.pending, target=STATUS.approved)
    def approve(self):
        # TODO: Add notification for approve
        with transaction.atomic():
            self.user.is_researcher = True
            self.response_date = timezone.now()
            self.user.save()
            self.save()

    @transition(field=status, source=STATUS.pending, target=STATUS.denied)
    def deny(self):
        # TODO: Add notification for deny
        with transaction.atomic():
            self.response_date = timezone.now()
            self.save()
