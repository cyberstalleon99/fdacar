from django.db import models
from masterlist.models import Establishment, Person
from masterlist import constants
from datetime import datetime
from dateutil.relativedelta import relativedelta
from accounts.models import User

class Record(models.Model):
    establishment =     models.OneToOneField(Establishment, on_delete=models.SET_NULL, null=True, blank=False)
    folder_id =         models.CharField(max_length=10, null=True, verbose_name="Folder Number")

    def __str__(self):
        try:
            # Check if Establishment has a folder
            self.establishment.name
        except:
            return "No file"
        else:
            return self.establishment.name + "(" + self.folder_id + ")"

    def get_last_inspection(self):
        try:
            self.inspections.latest().date_inspected
        except:
            return 'For inspection'
        else:
                return self.inspections.latest().date_inspected

    def get_inspection_type(self):
        try:
            self.inspections.latest().inspection_type.name
        except:
            return 'For inspection'
        else:
            return self.inspections.latest().inspection_type.name

    def get_next_inspection(self):
        next_date_inspection = ''

        try:
            self.inspections.latest()
        except:
            return 'For inspection'
        else:
            frequency_of_inspection = self.inspections.latest().frequency_of_inspection
            if frequency_of_inspection:
                next_date_inspection = self.inspections.latest().date_inspected + relativedelta(years=int(frequency_of_inspection))
            else:
                return 'No Risk Assessment'
        return next_date_inspection

class CapaPreparator(Person):
    # capa = models.OneToOneField(Capa, on_delete=models.CASCADE, null=True)
    designation =       models.CharField(max_length=255, choices=constants.ALL_DESIGNATIONS, null=True, blank=False)

    class Meta:
        verbose_name = 'Preparedy by'
        verbose_name_plural = 'Prepared by'

class Capa(models.Model):
    date_prepared =     models.DateField('Date Prepared', help_text='Format: YYYY/MM/DD')
    prepared_by =       models.ForeignKey(CapaPreparator, on_delete=models.PROTECT, null=True, blank=False)
    date_submitted =    models.DateField('Date Submitted', help_text='Format: YYYY/MM/DD')
    approved_by =       models.ForeignKey(User, on_delete=models.CASCADE)
    date_approved =     models.DateField('date_approved', help_text='Format: YYYY/MM/DD')
    remarks =           models.TextField(max_length=500, null=True, blank=True)
    recommendation =    models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        try:
            self.inspection.record.establishment.name
        except:
            dateStr = self.date_prepared.strftime("%d %b %Y ")
        else:
            dateStr = self.inspection.record.establishment.name + "(" + self.date_prepared.strftime("%d %b %Y ") + ")"
        return dateStr

class CapaDeficiency(models.Model):
    type =                      models.CharField(max_length=10, choices=constants.CAPA_TYPES)
    capa =                      models.ForeignKey(Capa, on_delete=models.SET_NULL, null=True, blank=True)
    description =               models.CharField(max_length=300)
    action =                    models.TextField()
    evidence =                  models.FileField(blank=True)

    proposed_completion_date =  models.DateField(verbose_name="Proposed Completion Date", null=True, blank=True)
    inspector_comment =         models.TextField(max_length=300, blank=True)
    accepted =                  models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'CAPA Deficiencies'
        verbose_name_plural = 'CAPA Deficiencies'

def report_directory_path(instance, filename):
    return 'masterlist/inspection/ir_{0}/{1}'.format(instance.record.establishment.id, filename)

class TypeOfInspection(models.Model):
    name = models.CharField(max_length=250)
    short_name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Inspection(models.Model):
    record =                        models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, verbose_name="Record", related_name="inspections")
    tracking_number =               models.CharField(max_length=14, null=True, verbose_name="DTN or Case #", help_text="Put N/I if no DTN")
    capa =                          models.OneToOneField(Capa, on_delete=models.SET_NULL, null=True, blank=True)
    # type_of_inspection =            models.CharField(max_length=250, choices=constants.INSPECTION_TYPES)
    inspection_type =               models.ForeignKey(TypeOfInspection, on_delete=models.CASCADE, null=True, verbose_name="Type of Inspection")
    date_inspected =                models.DateField('Date Inspected', help_text='Format: YYYY/MM/DD')
    frequency_of_inspection =       models.PositiveIntegerField(default=0, verbose_name="Frequency of Inspection", null=True, blank=True, help_text="Leave blank if not applicable")
    risk_rating =                   models.CharField(max_length=7, choices=constants.RISK_RATINGS, null=True, blank=True, help_text="Leave blank if not applicable")
    date_of_followup_inspection =   models.DateField('Date of Followup Inspection', null=True, blank=True, help_text='Format: YYYY/MM/DD')
    remarks =                       models.TextField(null=True, help_text="Put inspection remarks here. Number each remark.")
    date_forwarded =                models.DateField('Date Forwarded to Supervisor', null=True, blank=True, help_text='Format: YYYY/MM/DD')
    date_approved =                 models.DateField('Date Approved by Supervisor', null=True, blank=True, help_text='Format: YYYY/MM/DD')
    for_capa =                      models.BooleanField(default=False)
    inspection_report =             models.FileField(null=True, blank=True, upload_to=report_directory_path, verbose_name='Inspection Report')

    def __str__(self):
        dateStr = self.date_inspected.strftime("%d %b %Y ")
        name = self.record.establishment.name
        return name + " - " + self.tracking_number + "(" + dateStr + ")"

    def get_followup_duration(self):
        month = 0
        if self.date_of_followup_inspection:
            start_date = datetime.now().date()
            end_date = self.date_of_followup_inspection
            difference = relativedelta(end_date, start_date)
            month = difference.years * 12 + difference.months
        return month

    def get_next_inspection(self):
        next_date_inspection = ''
        try:
            self.date_inspected + relativedelta(years=int(self.frequency_of_inspection))
        except:
            return 'For inspection'
        else:
            frequency_of_inspection = self.frequency_of_inspection
            if frequency_of_inspection:
                next_date_inspection = self.date_inspected + relativedelta(years=int(frequency_of_inspection))
            else:
                return 'No Risk Assessment'
            return next_date_inspection

    class Meta:
        ordering = ['-date_inspected']
        get_latest_by = 'date_inspected'

class EstInspector(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name="est_inspectors")
    inspector = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.inspector.get_short_name()

def capa_attachments_directory_path(instance, filename):
    return 'masterlist/inspection/attachments/report_{0}/{1}'.format(instance.capa.id, filename)
