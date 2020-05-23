from django.db import models
from django.utils import timezone
from masterlist import constants
from masterlist.models import Establishment
from .mymanagers import RenewalChecklistManager, PLIChecklistManager, RoutineListManager

class Job(models.Model):
    establishment = models.OneToOneField(Establishment, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField('Date Created', default=timezone.now)
    inspection_status = models.CharField(max_length=11, default=constants.INSPECTION_STATUS[1])
    inspection_type = models.CharField(max_length=20, choices=constants.INSPECTION_TYPES, null=True)
    renchecklist = RenewalChecklistManager()
    plichecklist = PLIChecklistManager()
    routinelist = RoutineListManager()
    # followuplist =
    objects = models.Manager()

    def __str__(self):
        return self.establishment.name

    class Meta:
        ordering = ['establishment__ltos__expiry']
