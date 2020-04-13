
from datetime import datetime
from django.db import models
from . import myhelpers
from . import constants


class ExpiredListManager(myhelpers.MyModelManager):

    def get(self, establishments):
        checklist = []
        for est in establishments:
            if est.ltos.first().expiry.date() < datetime.now().date():
                checklist.append(est)
        return checklist

class RenewalChecklistManager(myhelpers.MyModelManager):

    except_activities = ['Hospital Pharmacy', 'Medical X-Ray', 'Veterinary X-Ray', 'Dental X-Ray', 'Educational X-Ray', 'MRI', 'CTScan']

    def get(self, establishments):
        checklist = []
        from checklist.models import Job
        print(establishments)
        for est in establishments:
            # inspection status = {'0': inspected, '1': pending}
            # checklist status = {'0': hidden, '1': visible}

            if est.ltos.first().get_duration() <= 6 and est.specific_activity.filter(name__in=self.except_activities).exists()==False and est.inspection_set.all().count() != 0:
                print(est)
                if Job.objects.filter(establishment_id=est.id).exists()==False: # create a job object if est is not existing in Job model
                    print('.............................')
                    Job.objects.create(establishment=est, inspection_type=constants.INSPECTION_TYPES[1][0])


        return Job.objects.filter(inspection_type=constants.INSPECTION_TYPES[1][0])

class PLIChecklistManager(myhelpers.MyModelManager):

    def get(self, establishments):
        checklist = []
        for est in establishments:
            if est.inspection_set.all().count() == 0:
                checklist.append(est)
        return checklist

class RoutineListManager(myhelpers.MyModelManager):

    def get(self):
        checklist = []
        for est in establishments:
            if est.inspection_set.first(): # check if establishment has inspections
                if est.inspection_set.first().get_followup_duration() <= 6:
                    checklist.append(est)
        return checklist
