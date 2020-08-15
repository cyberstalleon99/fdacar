from django.db import models
from . import constants
from masterlist.models import Establishment, VariationType
from records.models import Inspection
from accounts.models import User
DEFAULT_SUPERVISOR_ID = 7

class Application(models.Model):
    status  =                       models.CharField(max_length=250, choices=constants.APPLICATION_STATUS)
    tracking_number =               models.CharField(max_length=12, verbose_name="DTN/Case No.")
    group =                         models.DateField(verbose_name="Month")
    applied_thru =                  models.CharField(max_length=250, choices=constants.APPLIED_THRU)
    establishment =                 models.ForeignKey(Establishment, on_delete=models.PROTECT)
    application_type =              models.CharField(max_length=250, choices=constants.APPLICATIONS)
    type_of_variation =             models.ForeignKey(VariationType, on_delete=models.CASCADE, null=True, blank=True)
    payment =                       models.DecimalField(max_digits=10, decimal_places=2)

    date_received_by_rfo =          models.DateField(verbose_name="Date Posted/Received")
    date_forwarded_to_inspector =   models.DateField(null=True, blank=True)
    date_received_by_inspector =    models.DateField(null=True, blank=True)
    inspection =                    models.ForeignKey(Inspection, on_delete=models.PROTECT, null=True, blank=True)
    date_accomplished =             models.DateField(verbose_name="Eportal Accomplishment Date", null=True, blank=True)
    recommendation =                models.CharField(max_length=20, choices=constants.RECOMMENDATION)

    licensing_officer =             models.ForeignKey(User, on_delete=models.DO_NOTHING, default=DEFAULT_SUPERVISOR_ID)
    date_received_by_supervisor =   models.DateField(verbose_name="Date Received by Supervisor (eportal)", null=True, blank=True)
    date_approved_by_supervisor =   models.DateField(verbose_name="Date Approved by Supervisor (eportal)", null=True, blank=True)
    processing_duration =           models.PositiveIntegerField(null=True, blank=True)
    eod_1 =                         models.CharField(max_length=3, choices=constants.YESORNO, verbose_name="w/in ARTA (w/o inspection)", null=True, blank=True)
    eod_2 =                         models.CharField(max_length=3, choices=constants.YESORNO, verbose_name="w/in ARTA (w/ inspection)", null=True, blank=True)
    backlog =                       models.CharField(max_length=3, choices=constants.YESORNO, null=True, blank=True)
    reason_1 =                      models.TextField(verbose_name="Reason for Backlog", null=True, blank=True)
    date_forwarded_to_center_1 =    models.DateField(verbose_name="Date Forwarded to Center", null=True, blank=True)
    date_returned_by_center =       models.DateField(null=True, blank=True)
    reason_2 =                      models.TextField(verbose_name="Reason", null=True, blank=True)
    date_forwarded_to_center_2 =    models.DateField(verbose_name="Date Forwarded to Center", null=True, blank=True)

    def __str__(self):
        return self.establishment.name + " - " + self.tracking_number