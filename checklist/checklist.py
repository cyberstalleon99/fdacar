from .models import Job
from masterlist.models import Establishment
from masterlist import constants

class Checklist:

    class Renewal:
        excluded_activities = ['Hospital Pharmacy', 'Medical X-Ray', 'Veterinary X-Ray', 'Dental X-Ray', 'Educational X-Ray', 'MRI', 'CTScan']
        establishments = Establishment.objects.filter(status='Active').exclude(specific_activity__name__in=excluded_activities)

        def create_jobs(self):
            for est in self.establishments:
                if est.ltos.latest().get_duration() <= 6:
                    if Job.objects.filter(establishment_id=est.id).exists()==False:
                        Job.objects.create(establishment=est, job_type=constants.JOB_TYPES[1][0], inspection_status=constants.INSPECTION_STATUS[1][0])
                    else:
                        if Job.objects.filter(establishment_id=est.id).first().inspection_status==constants.INSPECTION_STATUS[0][0]:
                            Job.objects.create(establishment=est, job_type=constants.JOB_TYPES[1][0])

        def get_list(self):
            self.create_jobs()
            return Job.objects.get_queryset().filter(job_type=constants.JOB_TYPES[1][0], inspection_status=constants.INSPECTION_STATUS[1][0])