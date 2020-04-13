
from datetime import datetime
from django.db import models
from . import myhelpers
from . import constants
from django.db.models import Q

class ExpiredListManager(myhelpers.MyModelManager):

    def get_list(self):
        establishments = super().get_queryset().all()
        checklist = []
        for est in establishments:
            if est.ltos.first().expiry.date() < datetime.now().date():
                checklist.append(est)
        return checklist

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
        checklist = []
        for est in establishments:
            if est.ltos.first().expiry.date() < datetime.now().date():
                checklist.append(est)
        return checklist

from datetime import datetime

from django.db import models

class ActiveManager(models.Manager):

    def __init__(self, from_date=None, to_date=None):
        super(ActiveManager, self).__init__()
        print(to_date)
        self.from_date = from_date
        self.to_date = to_date
        now = datetime.now
        if from_date and to_date:
            self.date_filters = (models.Q(**{'%s__isnull' % self.to_date: True}) |
                                 models.Q(**{'%s__gte' % self.to_date: now}),
                                 models.Q(**{'%s__isnull' % self.from_date: True}) |
                                 models.Q(**{'%s__lte' % self.from_date: now}))

        elif from_date:
            self.date_filters = (models.Q(**{'%s__isnull' % self.from_date: True}) |
                                 models.Q(**{'%s__lte' % self.from_date: now}),)
        elif to_date:
            self.date_filters = (models.Q(**{'%s__isnull' % self.to_date: True}) |
                                 models.Q(**{'%s__gte' % self.to_date: now}),)
        else:
            raise ValueError

    def get_query_set(self):
        """Retrieves items with publication dates according to self.date_filters
        """
        return super(ActiveManager, self).get_query_set().filter(*self.date_filters)
