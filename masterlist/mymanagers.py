
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

    def get(self, establishments):
        checklist = []
        for est in establishments:
            # # if establishment's LTO's duration is less than 6mos. and inspection status = inspected and checklist status = notok
            # if est.ltos.first().get_duration() <= 6 and  est.inspection_status == constants.INSPECTION_STATUS[0] and est.checklist_status == constants.CHECKLIST_STATUS[0]:
            #     est.inspection_status == constants.INSPECTION_STATUS[1]
            #
            # # if establishment's LTO's duration is less than 6mos. and inspection status = uninspected
            # if est.ltos.first().get_duration() <= 6 and  est.inspection_status == constants.INSPECTION_STATUS[1]:
            #     checklist.append(est)

            except_activities = est.specific_activity.objects.get(pk=4)

            if est.ltos.first().get_duration() <= 6:
                # print(est.specific_activity.all())
                if except_activities in est.specific_activity.all():
                    print('Andito po siya............')
                else:
                    print('Not in the specific_activity............')



        return checklist

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
