from django.db import models
from incoming.models import DocumentType
from accounts.models import User

class Courier(models.Model):
    name = models.CharField(max_length=250, verbose_name="Courier Name")

    def __str__(self):
        return self.name

class Outgoing(models.Model):
    group = models.DateField(verbose_name='Group')
    dtn = models.CharField(max_length=14, verbose_name="DTN")
    document_type = models.OneToOneField(DocumentType, on_delete=models.CASCADE, verbose_name="Type of Document")
    particulars = models.TextField()
    remarks = models.TextField()
    courier = models.OneToOneField(Courier, on_delete=models.CASCADE, verbose_name="Courier Name")
    courier_tracking_number = models.CharField(max_length=250, verbose_name = "Courier Tracking No.")
    date_forwarded = models.DateField(verbose_name="Date Forwarded/Mailed")
    forwarded_by = models.OneToOneField(User, on_delete=models.CASCADE)
    forwarded_to = models.CharField(max_length=250, verbose_name="Forwarded To")
    forwarded_to_1 = models.CharField(max_length=250, verbose_name="Forwarded To (Company/Office Name)")

    def __str__(self):
        return self.dtn

