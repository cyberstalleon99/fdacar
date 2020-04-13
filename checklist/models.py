from django.db import models
from django.utils import timezone
from masterlist import constants
from masterlist.models import Establishment

class Job(models.Model):
    establishment = models.OneToOneField(Establishment, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField('Date Created', default=timezone.now)
    inspection_status = models.CharField(max_length=11, default=constants.INSPECTION_STATUS[1])
    inspection_type = models.CharField(max_length=20, choices=constants.INSPECTION_TYPES, null=True)

    def __str__(self):
        return self.establishment.name
