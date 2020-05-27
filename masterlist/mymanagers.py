from django.utils import timezone
from . import myhelpers
from django.db import models

class ExpiredListManager(myhelpers.MyModelManager):

    def get_list(self):
        establishments = set()
        for est in super().get_queryset():
            if est.ltos.latest().expiry < timezone.now().date():
                establishments.add(est.id)

        return super().get_queryset().filter(pk__in=establishments)

class InactiveListManager(models.Manager):

    def get_list(self):
        return super().get_queryset().filter(status='Inactive')
