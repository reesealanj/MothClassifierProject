import json
import redis
import time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from classifications.models import Classification
from classifications.services import update_classification
from constants import MIN_ACCURACY, ML_CHANNEL, REDIS_HOST, REDIS_PORT
from jobs.models import Job
from conf.secrets import REDIS_PASS


POLL_TIME = 1


class Command(BaseCommand):
    help = 'Starts listening for messages from the Machine Learning service'

    def handle(self, *args, **options):
        # Connect to the redis server
        redis_server = redis.StrictRedis(
            host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASS
        )
        redis_sub = redis_server.pubsub(ignore_subscribe_messages=True)
        redis_sub.subscribe(ML_CHANNEL)

        # Listen indefinitely or program exits
        while True:
            message = redis_sub.get_message()
            # Check if there is a message
            if message is not None:
                data = json.loads(message['data'])
                self.update_job(data)

        time.sleep(POLL_TIME)

    def update_job(self, data):
        """
        Updates a job with the job_data

        Parameters
        ----------
        data: dict
            A dictionary containing data about the job
            {
                'job': int,
                'species': str,
                'accuracy: float,
            }
        """

        job = Job.objects.get(id=data.pop('job'))
        classification = Classification.objects.get(image=job.image)

        data['is_automated'] = True
        data['needs_review'] = False if data.get('accuracy') > MIN_ACCURACY else True
        print(f'[{timezone.now()}: INFO/UpdateJob]: {data}')
        update_classification(classification, data)

        job.finish()
        job.save()
