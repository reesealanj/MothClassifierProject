# Handles the jobs sent from the Moth Classifier API
import json
import redis
import requests
import sys
import time

from config.passwords import REDIS_PASS
from config.secrets import API_URL
from constants import API_JOB_CHANNEL, ML_CHANNEL, REDIS_HOST, REDIS_PORT

sys.path.append('.')
from mmodel import MModel

POLL_TIME = 1

def get_prediction(model_file, image_id):
    """
    Gets the prediction for the specified image with the specified model

    Parameters
    ----------
    model_file: str
        The .h5 file (saved and trained model) to use for the prediction
    image_id: int
        The id assigned to this image from the Moth Classifier API

    Returns
    -------
    dict
        A dictionary that holds the prediction and necessary metadata
        {
            'species': str,
            'accuracy': float,
        }
    """
    model = MModel(
        '5_species_model',
        'CLASSIFIER',
        '5 species model',
        6,
        model=model_file,
    )

    # Get the image from the Moth Classifier API
    response = requests.get(f'{API_URL}images/{image_id}')

    # Run the specified model on the image
    species, accuracy = model.test(url=response.json().get('file'), name=str(image_id), is_local=False)
    return {
        'species': species,
        'accuracy': accuracy,
    }


def main():
    redis_server = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASS)
    redis_sub = redis_server.pubsub()
    redis_sub.subscribe(API_JOB_CHANNEL)

    # Listen indefinitely until exit
    while True:
        message = redis_sub.get_message(ignore_subscribe_messages=True)
        # Check if there is a message and make sure is the correct type
        if message is not None:
            data = json.loads(message['data'])

            prediction = get_prediction(data.get('model_file'), data.get('image'))
            prediction['job'] = data.get('job')

            # Send the prediction back to the Moth Classifier API
            redis_server.publish(ML_CHANNEL, json.dumps(prediction))

        time.sleep(POLL_TIME)

main()
