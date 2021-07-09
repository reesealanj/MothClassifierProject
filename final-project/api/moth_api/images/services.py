from celery.decorators import task
from celery.utils.log import get_task_logger
import csv
import os
from zipfile import ZipFile, ZIP_DEFLATED

from django.conf import settings

from constants import TRAINING_FILE, TRAINING_REFRESH_SIZE
from images.models import Image


logger = get_task_logger(__name__)


def generate_zip_file(params, images, file_name, metadata_name, append=False):
    species_folders = set()
    mode = 'a' if append else 'w'

    with ZipFile(file_name, mode, ZIP_DEFLATED) as zip_file:
        for image in images:
            path = image.file.path
            species_folders.add(os.path.dirname(path))
            zip_file.write(path, arcname=path[path.find(settings.MEDIA_URL) :])

    # Record the URL parameters, the species, and number of images for each species in the metadata file
    species_folders = sorted(
        species_folders, key=lambda folder: len(os.listdir(folder)), reverse=True
    )

    with open(metadata_name, 'w', newline='') as metadata:
        writer = csv.writer(metadata)
        writer.writerow(['Parameters'])
        for k, v in params.items():
            writer.writerow([k, v])

        writer.writerow('')
        writer.writerow(['Folders'])

        for folder in species_folders:
            writer.writerow([os.path.basename(folder), len(os.listdir(folder))])

    with ZipFile(file_name, 'a', ZIP_DEFLATED) as zip_file:
        zip_file.write(metadata_name)

    # Clean up
    try:
        os.remove(metadata_name)
    except:
        pass


def download_images(request, images):
    # Add all the images to the zip file
    file_name = 'dataset.zip'
    metadata_name = 'metadata.csv'

    # Special exception for training data (?is_training=true)
    if (
        len(request.query_params) == 1
        and list(request.query_params.items())[0][0] == 'is_training'
        and list(request.query_params.items())[0][1]
    ):
        file_name = TRAINING_FILE
        if os.path.exists(file_name):
            return file_name, None

    generate_zip_file(request.query_params, images, fle_name, metadata_name)

    return file_name, metadata_name


# This function will generate the training dataset zip file
@task(name='create_training_dataset')
def create_training_dataset():
    logger.info('Checking if training dataset needs to be updated')
    # Get the training dataset
    images = Image.objects.filter(is_training=True).order_by('-id')

    # Count how many images are in the training zip file
    try:
        with ZipFile(TRAINING_FILE, 'r', ZIP_DEFLATED) as zip_file:
            zip_count = len(zip_file.namelist()) - 1  # Ignore the metadata.csv file
    except:
        zip_count = 0
        with ZipFile(TRAINING_FILE, 'w', ZIP_DEFLATED) as zip_file:
            pass

    params = {
        'is_training': True,
    }

    logger.info(
        f'Updating training dataset\nImages: {images.count()}\nZip Count: {zip_count}'
    )
    if images.count() - zip_count >= TRAINING_REFRESH_SIZE:
        # Rebuild the zip file
        generate_zip_file(
            params,
            images[: images.count() - zip_count],
            TRAINING_FILE,
            'metadata.csv',
            append=True,
        )
        logger.info('Updated training dataset')
