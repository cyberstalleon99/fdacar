from django.db import models
from accounts.models import User

class DocumentType(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

# Create your models here.
class Incoming(models.Model):
    group = models.DateField(verbose_name='Group')
    dtn = models.CharField(max_length=14, verbose_name="DTN")
    date_received = models.DateField(verbose_name='Date Received', help_text='Format: YYYY/MM/DD')
    received_by = models.OneToOneField(User, on_delete=models.CASCADE)
    received_from = models.CharField(max_length=250, verbose_name="Received from")
    received_from_1 = models.CharField(max_length=250, verbose_name="Received from (Company/Establishment Name)")
    document_type = models.OneToOneField(DocumentType, on_delete=models.CASCADE, verbose_name="Type of Document")
    particulars = models.TextField()
    endorsed_to = models.CharField(max_length=250, verbose_name="Endorsed to")
    date_endorsed = models.DateField(verbose_name='Date Endorsed', help_text='Format: YYYY/MM/DD')
    date_acted_upon = models.DateField(verbose_name="Date Acted Upon", help_text='Format: YYYY/MM/DD')
    actions_taken = models.TextField()

    def __str__(self):
        return self.dtn

