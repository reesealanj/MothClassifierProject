import json
from model_bakery import baker
import os
import redis
from unittest.mock import patch

from rest_framework.test import APITestCase

from constants import API_JOB_CHANNEL
from jobs.models import Job
from jobs.services import handle_job


class TestHandleJob(APITestCase):
    """
    Test module the handle_job service
    """

    def setUp(self):

        self.image = baker.make('images.Image', _create_files=True)
        self.job = baker.make(
            'jobs.Job', job_type=Job.JOB_TYPE.classify, image=self.image
        )

    def tearDown(self):
        os.remove(self.image.file.path)

    def refresh_job(self):
        # Can't use refresh_from_db() due to the use of FSMField
        self.job = Job.objects.get(id=self.job.id)

    def test_error_if_ml_service_unvailable(self):
        """
        Ensure that the job errors if the Machine Learning service is unavailable
        """

        handle_job(self.job.id)
        self.refresh_job()

        self.assertEqual(self.job.status, Job.STATUS.error)

    def test_error_if_unsupported_job(self):
        """
        Ensure that the job errors if the job is unsupported
        """

        self.job.job_type = 'unsupported'
        self.job.save()

        with patch.object(
            redis.StrictRedis, 'pubsub_numsub', return_value=[(API_JOB_CHANNEL, 1)]
        ) as mock_method:
            handle_job(self.job.id)

        self.refresh_job()

        self.assertEqual(self.job.status, Job.STATUS.error)

    def test_successful_job(self):
        """
        Ensure that a valid job has the correct data
        """

        redis_server = redis.StrictRedis()
        redis_sub = redis_server.pubsub(ignore_subscribe_messages=True)
        redis_sub.subscribe(API_JOB_CHANNEL)
        model = baker.make('ml_models.MLModel', model_type='classifier')

        handle_job(self.job.id)
        self.refresh_job()

        msg = redis_sub.get_message()
        while msg is None:
            msg = redis_sub.get_message()

        data = json.loads(msg['data'])
        self.assertEqual(self.job.status, Job.STATUS.running)
        self.assertEqual(data.get('job'), self.job.id)
