from django.db import models
from masterlist.models import Establishment, Person
from masterlist import constants
from datetime import datetime
from dateutil.relativedelta import relativedelta
from accounts.models import User

class Record(models.Model):
    establishment = models.OneToOneField(Establishment, on_delete=models.SET_NULL, null=True, blank=False)
    folder_id = models.CharField(max_length=10, null=True, verbose_name="Folder Number")

    def __str__(self):
        return self.establishment.name + "(" + self.folder_id + ")"

class Capa(models.Model):
    start_date = models.DateTimeField('start_date')
    approved_by = models.CharField(max_length=10, choices=constants.INSPECTORS)
    date_submitted = models.DateTimeField('date_submitted', help_text='Format: YYYY/MM/DD')
    date_approved = models.DateTimeField('date_approved', help_text='Format: YYYY/MM/DD')
    remarks = models.CharField(max_length=200)

    def __str__(self):
        dateStr = self.start_date.strftime("%d %b %Y ")
        return dateStr

class CapaPreparator(Person):
    capa = models.OneToOneField(Capa, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Preparedy by'
        verbose_name_plural = 'Prepared by'

class CapaDeficiency(models.Model):
    capa = models.ForeignKey(Capa, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=200)
    action = models.CharField(max_length=200)
    evidence = models.FileField(blank=True)

    type = models.CharField(max_length=10, choices=constants.CAPA_TYPES)
    proposed_comletion_date = models.DateTimeField(verbose_name="Proposed Completion Date")
    inspector_comment = models.CharField(max_length=200, blank=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'CAPA Deficiencies'
        verbose_name_plural = 'CAPA Deficiencies'

def report_directory_path(instance, filename):
    return 'masterlist/inspection/ir_{0}/{1}'.format(instance.record.establishment.id, filename)

class Inspection(models.Model):
    record = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, verbose_name="Record")
    tracking_number = models.CharField(max_length=14, null=True, verbose_name="DTN or Case #")
    capa = models.OneToOneField(Capa, on_delete=models.SET_NULL, null=True, blank=True)
    type_of_inspection = models.CharField(max_length=20, choices=constants.INSPECTION_TYPES)
    date_inspected = models.DateTimeField('Date Inspected', help_text='Format: YYYY/MM/DD')
    frequency_of_inspection = models.PositiveIntegerField(default=0, verbose_name="Frequency of Inspection", null=True, blank=True)
    risk_rating = models.CharField(max_length=7, choices=constants.RISK_RATINGS, null=True, blank=True)
    date_of_followup_inspection = models.DateTimeField('Date of Followup Inspection', null=True, blank=True, help_text='Format: YYYY/MM/DD')
    # inspector = models.CharField(max_length=3, choices=constants.INSPECTORS)
    inspector = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=200, null=True)
    inspection_report = models.FileField(null=True, blank=False, upload_to=report_directory_path, verbose_name='Inspection Report')

    def __str__(self):
        dateStr = self.date_inspected.strftime("%d %b %Y ")
        return dateStr

    def get_followup_duration(self):
        month = 0
        if self.date_of_followup_inspection:
            start_date = datetime.now().date()
            end_date = self.date_of_followup_inspection.date()
            difference = relativedelta(end_date, start_date)
            month = difference.years * 12 + difference.months
        return month

    class Meta:
        ordering = ['-date_inspected']
        get_latest_by = 'date_inspected'

def capa_attachments_directory_path(instance, filename):
    return 'masterlist/inspection/attachments/report_{0}/{1}'.format(instance.capa.id, filename)
