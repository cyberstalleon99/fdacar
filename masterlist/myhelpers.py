from django.db.models import Q
from django.db import models

class MyModelManager(models.Manager):

    def get_filtered_establishments(self, query):
        establishments = super().get_queryset().filter(
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

    def get_filtered_list(self, query):
        establishments = self.get_filtered_establishments(query=query)
        return self.get(establishments=establishments)

    def get_list(self):
        establishments = super().get_queryset()
        return self.get(establishments=establishments)

    def get(self, establishments):
        pass
