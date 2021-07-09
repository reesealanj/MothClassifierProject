from django.db import models

from constants import DEFAULT_SPECIES
from images.models import Image
from jobs.models import Job


class Classification(models.Model):

    species = models.CharField(max_length=40, default=DEFAULT_SPECIES)
    accuracy = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    image = models.OneToOneField(
        Image, on_delete=models.CASCADE, related_name='image_of', primary_key=True
    )
    is_automated = models.BooleanField(default=True)
    needs_review = models.BooleanField(default=False)
