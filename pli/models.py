from django.db import models
from records.models import Inspection

class PliStatus(models.Model):
    status = models.CharField(max_length=250)
    # Awaiting CAPA, For submission of Letter of Closure, Complete

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "PLI Status"

class Pli(models.Model):
    status = models.ForeignKey(PliStatus, on_delete=models.CASCADE)
    group = models.DateField(verbose_name="Month")
    mother_dtn = models.CharField(max_length=50, null=True, blank=True)
    inspection = models.ForeignKey(Inspection, on_delete=models.DO_NOTHING)
    date_forwarded_to_center = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.inspection.tracking_number

    class Meta:
        verbose_name_plural = "PLI's"

