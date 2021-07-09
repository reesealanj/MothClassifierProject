from django.db import models
from django_fsm import FSMField, transition
from fcm_django.models import FCMDevice
from model_utils import Choices

from images.models import Image
from ml_models.models import MLModel


class Job(models.Model):

    JOB_TYPE = Choices(('classify', 'classify', 'CLASSIFY'),)

    STATUS = Choices(
        ('issued', 'issued', 'ISSUED'),
        ('running', 'running', 'RUNNING'),
        ('done', 'done', 'DONE'),
        ('error', 'error', 'ERROR'),
    )

    job_type = models.CharField(
        max_length=15, choices=JOB_TYPE, default=JOB_TYPE.classify
    )
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    date_issued = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = FSMField(default=STATUS.issued, choices=STATUS, protected=True)
    status_message = models.CharField(max_length=200, blank=True)
    models = models.ManyToManyField(MLModel)

    # Implement the FSM for status
    @transition(field=status, source=STATUS.issued, target=STATUS.running)
    def run(self):
        pass

    @transition(field=status, source=STATUS.running, target=STATUS.done)
    def finish(self):
        devices = FCMDevice.objects.filter(user=self.image.user)
        devices.send_message(
            title='Job Completed',
            body=f'Your {self.job_type} job with id #{self.id} is compelete.',
            data={
                'click_action': 'FLUTTER_NOTIFICATION_CLICK',
                'title': 'Job Completed',
                'body': f'Your {self.job_type} job with id #{self.id} is compelete.',
            },
        )

    @transition(
        field=status, source=[STATUS.running, STATUS.issued], target=STATUS.error
    )
    def error(self, msg):
        self.status_message = msg
        self.save()

        devices = FCMDevice.objects.filter(user=self.image.user)
        devices.send_message(
            title='Job Failed',
            body=f'Your {self.job_type} job with id #{self.id} has failed.\nError: {msg}',
            data={
                'click_action': 'FLUTTER_NOTIFICATION_CLICK',
                'title': 'Job Failed',
                'body': f'Your {self.job_type} job with id #{self.id} has failed.\nError: {msg}',
            },
        )
