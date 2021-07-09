import os
import shutil

from django.conf import settings
from django.db import IntegrityError, transaction

from classifications.models import Classification


def update_classification(classification, data):
    # Move the image to its respective species' folder
    folder = data.get('species', classification.species)
    full_path = f'{settings.MEDIA_ROOT}{folder}/'
    if not os.path.exists(full_path):
        os.mkdir(full_path)

    try:
        shutil.move(classification.image.file.path, full_path)
    except (shutil.Error, FileExistsError):
        pass

    # Update the model with the new data
    with transaction.atomic():
        Classification.objects.filter(image=classification.image).update(**data)
        classification.image.file = f'{folder}/{os.path.split(classification.image.file.name)[1]}'  # Relative to MEDIA_ROOT
        classification.image.save()

    return classification
