from django.db import models
# from django.utils import timezone
from masterlist import constants
from masterlist.models import Establishment
from .mymanagers import RenewalChecklistManager, PLIChecklistManager, RoutineListManager

class Job(models.Model):
    establishment =     models.OneToOneField(Establishment, on_delete=models.CASCADE)
    date_created =      models.DateField('Date Created', auto_now_add=True)
    inspection_status = models.CharField(max_length=250, choices=constants.INSPECTION_STATUS)
    job_type =          models.CharField(max_length=250, choices=constants.JOB_TYPES, null=True)
    renchecklist =      RenewalChecklistManager()
    plichecklist =      PLIChecklistManager()
    routinelist =       RoutineListManager()
    # followuplist =
    objects = models.Manager()

    def __str__(self):
        return self.establishment.name

    class Meta:
        ordering = ['establishment__ltos__expiry']
