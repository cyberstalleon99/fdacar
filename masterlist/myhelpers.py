from django.db.models import Q
from django.db import models
from masterlist import constants

class MyModelManager(models.Manager):

    def check_for_inspection(self):
        pass

    def get_filtered_list(self, query):
        self.check_for_inspection()
        jobs = self.get_list().filter(
            Q(establishment__name__icontains=query) |
            Q(establishment__plant_address__address__icontains=query) |
            Q(establishment__plant_address__municipality_or_city__name__icontains=query) |
            Q(establishment__plant_address__region__name__icontains=query) |
            Q(establishment__plant_address__province__name__icontains=query) |
            Q(establishment__product_type__name__icontains=query) |
            Q(establishment__primary_activity__name__icontains=query) |
            Q(establishment__specific_activity__name__icontains=query) |
            Q(establishment__ltos__lto_number__icontains=query)
        ).distinct()
        return jobs

    def get_list(self):
        pass

    def get(self, establishments):
        pass
