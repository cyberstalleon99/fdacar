from masterlist.myhelpers import MyModelManager
from masterlist import constants

class RenewalChecklistManager(MyModelManager):
    except_activities = ['Hospital Pharmacy', 'Medical X-Ray', 'Veterinary X-Ray', 'Dental X-Ray', 'Educational X-Ray', 'MRI', 'CTScan']

    def create_jobs(self):
        from masterlist.models import Establishment
        for est in Establishment.objects.filter(status='Active'):
            try:
                est.record # Check if Establishment has a record
            except:
                # establishment has no inspections yet
                pass
            else:
                if est.ltos.latest().get_duration() <= 6 and \
                est.specific_activity.filter(name__in=self.except_activities).exists()==False:
                    if super().filter(establishment_id=est.id).exists()==False:
                        super().create(establishment=est, job_type=constants.JOB_TYPES[1][0], inspection_status=constants.INSPECTION_STATUS[1][0])
                    else:
                        if super().filter(establishment_id=est.id).first().inspection_status==constants.INSPECTION_STATUS[0][0]:
                            super().create(establishment=est, job_type=constants.JOB_TYPES[1][0])

    def get_list(self):
        self.create_jobs()
        jobs = super().get_queryset().filter(job_type=constants.JOB_TYPES[1][0], inspection_status=constants.INSPECTION_STATUS[1][0])
        return jobs

class PLIChecklistManager(MyModelManager):
    included_activities = ['Drugstore']

    def check_for_inspection(self):
        from masterlist.models import Establishment
        for est in Establishment.objects.filter(status='Active'):
            if est.specific_activity.filter(name__in=self.included_activities).exists()==True or est.primary_activity == 'Distributor':

                try:
                    est.record # Check if Establishment has a record
                except:
                    # establishment has no inspections yet
                    if  super().filter(establishment_id=est.id).exists()==False:
                        super().create(establishment=est, job_type=constants.JOB_TYPES[0])

            # check if est.lto.duration is renewed and establishment is still in the Job Checklist
            if est.ltos.latest().get_duration() > 6 and super().filter(establishment_id=est.id).exists():
                # check if it's PLI Type
                if super().get_queryset().get(establishment=est).job_type==constants.JOB_TYPES[0]:
                    super().get_queryset().get(establishment=est).delete()

    def get_list(self):
        # self.check_for_inspection()
        jobs = super().get_queryset().filter(job_type=constants.JOB_TYPES[0], inspection_status=constants.INSPECTION_STATUS[1])
        return jobs

class RoutineListManager(MyModelManager):

    def check_for_inspection(self):
        from masterlist.models import Establishment
        for est in Establishment.objects.all():
            if est.record.inspection_set.first(): # check if establishment has inspections
                if est.record.inspection_set.latest().get_followup_duration() <= 6:
                    if super().filter(establishment_id=est.id).exists()==False:
                        super().create(establishment=est, job_type=constants.JOB_TYPES[3])

            if est.ltos.latest().get_duration() > 6 and super().filter(establishment_id=est.id).exists():
                # check if it's RTN Type
                if super().get_queryset().get(establishment=est).job_type==constants.JOB_TYPES[3]:
                    super().get_queryset().get(establishment=est).delete()

    def get_list(self):
        # self.check_for_inspection()
        jobs = super().get_queryset().filter(job_type=constants.JOB_TYPES[3], inspection_status=constants.INSPECTION_STATUS[1])
        return jobs

class FollowupListManager(MyModelManager):

    def check_for_inspection(self):
        from masterlist.models import CapaDeficiency
        followup_list = CapaDeficiency.objects.filter(accepted=False)
        for capa_def in followup_list:
            est = capa_def.capa.inspection.establishment
            if super().filter(establishment_id=est.id).exists()==False:
                super().create(establishment=est, job_type=constants.JOB_TYPES[2])
