
from datetime import datetime
from django.db import models
from masterlist import myhelpers
from masterlist import constants
from django.db.models import Q

class RenewalChecklistManager(myhelpers.MyModelManager):

    except_activities = ['Hospital Pharmacy', 'Medical X-Ray', 'Veterinary X-Ray', 'Dental X-Ray', 'Educational X-Ray', 'MRI', 'CTScan']

    def check_for_inspection(self):
        from masterlist.models import Establishment
        for est in Establishment.objects.all():
            if est.ltos.first().get_duration() <= 6 and \
            est.specific_activity.filter(name__in=self.except_activities).exists()==False and \
            est.inspection_set.all().count() != 0:

                if super().filter(establishment_id=est.id).exists()==False:
                    super().create(establishment=est, inspection_type=constants.INSPECTION_TYPES[1][0])

    def get_list(self):
        self.check_for_inspection()
        jobs = super().get_queryset().filter(inspection_type=constants.INSPECTION_TYPES[1][0])
        return jobs

class PLIChecklistManager(myhelpers.MyModelManager):

    def check_for_inspection(self):
        from masterlist.models import Establishment
        for est in Establishment.objects.all():
            if est.specific_activity.filter(name__in='Drugstore').exists()==True and \
            est.primary_activity == 'Distributor' and \
            est.inspection_set.all().count() == 0:

                if super().filter(establishment_id=est.id).exists()==False:
                    super().create(establishment=est, inspection_type=constants.INSPECTION_TYPES[0][0])

    def get_list(self):
        self.check_for_inspection()
        jobs = super().get_queryset().filter(inspection_type=constants.INSPECTION_TYPES[0][0])
        return jobs

class RoutineListManager(myhelpers.MyModelManager):

    def check_for_inspection(self):
        from masterlist.models import Establishment
        for est in Establishment.objects.all():
            if est.inspection_set.first(): # check if establishment has inspections
                if est.inspection_set.first().get_followup_duration() <= 6:

                    if super().filter(establishment_id=est.id).exists()==False:
                        super().create(establishment=est, inspection_type=constants.INSPECTION_TYPES[3][0])

    def get_list(self):
        self.check_for_inspection()
        jobs = super().get_queryset().filter(inspection_type=constants.INSPECTION_TYPES[3][0])
        return jobs
