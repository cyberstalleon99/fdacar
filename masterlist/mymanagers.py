from django.utils import timezone
from . import myhelpers
from django.db.models import Q
from django.db import models

class ExpiredListManager(myhelpers.MyModelManager):

    def get_list(self):
        # establishments = super().get_queryset().filter(ltos__expiry__lt=timezone.now()).distinct()
        establishments = set()
        for est in super().get_queryset():
            if est.ltos.latest().expiry < timezone.now().date():
                establishments.add(est.id)

        return super().get_queryset().filter(pk__in=establishments)

    def get_filtered_list(self, query):
        establishments = self.get_list().filter(
            Q(name__icontains=query) |
            Q(plant_address__address__icontains=query) |
            Q(plant_address__municipality_or_city__name__icontains=query) |
            Q(plant_address__region__name__icontains=query) |
            Q(plant_address__province__name__icontains=query) |
            Q(product_type__name__icontains=query) |
            Q(primary_activity__name__icontains=query) |
            Q(specific_activity__name__icontains=query) |
            Q(ltos__lto_number__icontains=query)
        ).distinct()
        return establishments

class InactiveListManager(models.Manager):

    def get_list(self):
        return super().get_queryset().filter(status='Inactive')

    def get_filtered_list(self, query):
        establishments = self.get_list().filter(
            Q(name__icontains=query) |
            Q(plant_address__address__icontains=query) |
            Q(plant_address__municipality_or_city__name__icontains=query) |
            Q(plant_address__region__name__icontains=query) |
            Q(plant_address__province__name__icontains=query) |
            Q(product_type__name__icontains=query) |
            Q(primary_activity__name__icontains=query) |
            Q(specific_activity__name__icontains=query) |
            Q(ltos__lto_number__icontains=query)
        ).distinct()
        return establishments

