
from datetime import datetime
from django.db import models
from . import myhelpers

class ExpiredListManager(models.Manager):

    def get_filtered_list(self, query):
        establishments = myhelpers.get_filtered_establishments(query)
        checklist = []
        for est in establishments:
            if est.ltos.first().expiry.date() < datetime.now().date():
                checklist.append(est)
        return checklist


    def get_list(self):
        establishments = super().get_queryset()
        checklist = []
        for est in establishments:
            if est.ltos.first().expiry.date() < datetime.now().date():
                checklist.append(est)
        return checklist

class RenewalChecklistManager(models.Manager):

    def get_filtered_list(self, query):
        establishments = myhelpers.get_filtered_establishments(query)
        checklist = []
        for est in establishments:
            if est.ltos.first().get_duration() <= 6:
                checklist.append(est)
        return checklist

    def get_list(self):
        establishments = super().get_queryset()
        checklist = []
        for est in establishments:
            if est.ltos.first().get_duration() <= 6:
                checklist.append(est)
        return checklist

class PLIChecklistManager(models.Manager):

    def get_filtered_list(self, query):
        establishments = myhelpers.get_filtered_establishments(query)
        checklist = []
        for est in establishments:
            if est.inspection_set.all().count() == 0:
                checklist.append(est)
        return checklist

    def get_list(self):
        establishments = super().get_queryset()
        checklist = []
        for est in establishments:
            if est.inspection_set.all().count() == 0:
                checklist.append(est)
        return checklist

class RoutineListManager(models.Manager):

    def get_filtered_list(self, query):
        establishments = myhelpers.get_filtered_establishments(query)
        checklist = []
        for est in establishments:
            if est.inspection_set.first():
                if est.inspection_set.first().get_followup_duration() <= 6:
                    checklist.append(est)
        return checklist

    def get_list(self):
        establishments = super().get_queryset()
        checklist = []
        for est in establishments:
            if est.inspection_set.first():
                if est.inspection_set.first().get_followup_duration() <= 6:
                    checklist.append(est)
        return checklist
