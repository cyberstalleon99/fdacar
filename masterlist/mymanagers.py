
from datetime import datetime
from django.utils import timezone
from django.db import models
from . import myhelpers
from . import constants
from django.db.models import Q

class ExpiredListManager(myhelpers.MyModelManager):

    def get_list(self):
        establishments = super().get_queryset().filter(ltos__expiry__lt=timezone.now()).distinct()
        return establishments

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
        )
        return establishments
