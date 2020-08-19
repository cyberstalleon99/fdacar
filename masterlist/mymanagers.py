from django.utils import timezone
from . import myhelpers
from django.db import models

class ExpiredListManager(myhelpers.MyModelManager):

    def get_list(self):
        establishments = set()
        establishments.clear()
        for est in super().get_queryset().filter(status='Active'):
            try:
                est.ltos.latest().expiry
            except:
                pass
            else:
                if est.ltos.latest().expiry < timezone.now().date():
                    establishments.add(est.id)

        return super().get_queryset().filter(pk__in=establishments)

class ClosedManager(models.Manager):

    def get_list(self):
        return super().get_queryset().filter(status='Closed')

class InactiveManager(models.Manager):

    def get_list(self):
        return super().get_queryset().filter(status='Inactive')
