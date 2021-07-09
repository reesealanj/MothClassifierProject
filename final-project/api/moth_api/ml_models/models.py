from django.db import models
from model_utils import Choices


class MLModel(models.Model):

    MODEL_TYPE = Choices(
        ('detector', 'detector', 'DETECTOR'),
        ('classifier', 'classifier', 'CLASSIFIER'),
    )

    name = models.CharField(max_length=30, unique=True)
    file_name = models.CharField(max_length=30, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    model_type = models.CharField(max_length=15, choices=MODEL_TYPE)
    rating = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    comments = models.TextField(blank=True)
