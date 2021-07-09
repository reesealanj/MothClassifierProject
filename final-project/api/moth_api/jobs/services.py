from celery.decorators import task
from celery.utils.log import get_task_logger
import json
import redis
import time

from constants import API_JOB_CHANNEL, REDIS_HOST, REDIS_PORT
from jobs.models import Job
from ml_models.models import MLModel
from conf.secrets import REDIS_PASS


logger = get_task_logger(__name__)


@task(name='handle_job')
def handle_job(job_id):
    redis_server = redis.StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASS
    )
    job = Job.objects.get(pk=job_id)

    job.run()
    job.save()

    # Check if there is a subscriber on the API_JOB_CHANNEL
    # If there is no subscriber, error out the job
    if redis_server.pubsub_numsub(API_JOB_CHANNEL)[0][1] == 0:
        job.error('Machine Learning service is unavailable.')
        job.save()
        return

    if job.job_type == job.JOB_TYPE.classify:
        model = (
            MLModel.objects.filter(model_type=MLModel.MODEL_TYPE.classifier)
            .order_by('-rating')
            .first()
        )
    else:
        # Job is not supported yet
        # (Might be replaced if no new job types are needed)
        job.error('Job is not supported yet')
        job.save()
        return

    job.models.add(model)
    data = {
        'job': job.id,
        'model_file': model.file_name,
        'image': job.image.id,
    }

    logger.info(data)
    redis_server.publish(API_JOB_CHANNEL, json.dumps(data))
