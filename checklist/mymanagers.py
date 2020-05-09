from datetime import datetime
from django.db import models
from masterlist.myhelpers import MyModelManager
from masterlist import constants
from django.db.models import Q

class RenewalChecklistManager(MyModelManager):
    except_activities = ['Hospital Pharmacy', 'Medical X-Ray', 'Veterinary X-Ray', 'Dental X-Ray', 'Educational X-Ray', 'MRI', 'CTScan']

    def check_for_inspection(self):
        from masterlist.models import Establishment
        for est in Establishment.objects.all():
            if est.ltos.latest().get_duration() <= 6 and \
            est.specific_activity.filter(name__in=self.except_activities).exists()==False and \
            est.record.inspection_set.all().count() != 0:

                if super().filter(establishment_id=est.id).exists()==False:
                    super().create(establishment=est, inspection_type=constants.JOB_TYPES[1])

            # check if est.lto.duration is renewed and establishment is still in the Job Checklist
            if est.ltos.latest().get_duration() > 6 and super().filter(establishment_id=est.id).exists():
                # check if it's REN Type
                if super().get_queryset().get(establishment=est).inspection_type==constants.JOB_TYPES[1]:
                    super().get_queryset().get(establishment=est).delete()

    def get_list(self):
        self.check_for_inspection()
        jobs = super().get_queryset().filter(inspection_type=constants.JOB_TYPES[1], inspection_status=constants.INSPECTION_STATUS)
        return jobs

class PLIChecklistManager(MyModelManager):
    included_activities = ['Drugstore']

    def check_for_inspection(self):
        from masterlist.models import Establishment
        for est in Establishment.objects.all():
            if est.specific_activity.filter(name__in=self.included_activities).exists()==True or est.primary_activity == 'Distributor':
                if  est.record.inspection_set.all().count() == 0 and super().filter(establishment_id=est.id).exists()==False:
                    super().create(establishment=est, inspection_type=constants.JOB_TYPES[0])

            # check if est.lto.duration is renewed and establishment is still in the Job Checklist
            if est.ltos.latest().get_duration() > 6 and super().filter(establishment_id=est.id).exists():
                # check if it's PLI Type
                if super().get_queryset().get(establishment=est).inspection_type==constants.JOB_TYPES[0]:
                    super().get_queryset().get(establishment=est).delete()

    def get_list(self):
        self.check_for_inspection()
        jobs = super().get_queryset().filter(inspection_type=constants.JOB_TYPES[0], inspection_status=constants.INSPECTION_STATUS[1])
        return jobs

class RoutineListManager(MyModelManager):

    def check_for_inspection(self):
        from masterlist.models import Establishment
        for est in Establishment.objects.all():
            if est.record.inspection_set.first(): # check if establishment has inspections
                if est.record.inspection_set.latest().get_followup_duration() <= 6:
                    if super().filter(establishment_id=est.id).exists()==False:
                        super().create(establishment=est, inspection_type=constants.JOB_TYPES[3])

            # check if est.lto.duration is renewed and establishment is still in the Job Checklist
            if est.ltos.latest().get_duration() > 6 and super().filter(establishment_id=est.id).exists():
                # check if it's RTN Type
                if super().get_queryset().get(establishment=est).inspection_type==constants.JOB_TYPES[3]:
                    super().get_queryset().get(establishment=est).delete()

    def get_list(self):
        self.check_for_inspection()
        jobs = super().get_queryset().filter(inspection_type=constants.JOB_TYPES[3], inspection_status=constants.INSPECTION_STATUS[1])
        return jobs

class FollowupListManager(MyModelManager):

    def check_for_inspection(self):
        from masterlist.models import CapaDeficiency
        followup_list = CapaDeficiency.objects.filter(accepted=False)
        for capa_def in followup_list:
            est = capa_def.capa.inspection.establishment
            if super().filter(establishment_id=est.id).exists()==False:
                super().create(establishment=est, inspection_type=constants.JOB_TYPES[2])
