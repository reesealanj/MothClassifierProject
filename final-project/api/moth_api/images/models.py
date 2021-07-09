import imagehash
import PIL

from django.db import models

from constants import DEFAULT_SPECIES
from users.models import User


class Image(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=f'{DEFAULT_SPECIES}/')
    country = models.CharField(max_length=20, blank=True)
    region = models.CharField(max_length=20, blank=True)
    county = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    zip_code = models.PositiveIntegerField(null=True, blank=True)
    street = models.CharField(max_length=30, blank=True)
    lat = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    lng = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    date_taken = models.DateTimeField(auto_now_add=True)
    width = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    is_training = models.BooleanField(default=False)
    hash = models.CharField(max_length=16, null=True)

    class Meta:
        unique_together = ['user', 'hash']

    # Override the save() method to calculate the hash of the image
    def save(self, *args, **kwargs):
        self.hash = str(imagehash.phash(PIL.Image.open(self.file)))
        super(Image, self).save(*args, **kwargs)
