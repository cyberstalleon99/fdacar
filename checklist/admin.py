from django.contrib import admin
from .models import Job
from masterlist.admin import EstablishmentAdmin
from masterlist import constants
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    model = Job
    actions = ['mark_done']
    list_per_page = 20
    search_fields = ['establishment__name', 'establishment__ltos__lto_number']

    list_display = ('name', 'address', 'product_type', 'primary_activity', 'specific_activity',
                    'lto_number', 'expiry', 'job_type', 'inspection_status', 'last_inspection'
    )

    list_filter = (
        ('establishment__name', DropdownFilter),
        ('establishment__product_type', RelatedDropdownFilter),
        ('establishment__primary_activity', RelatedDropdownFilter),
        ('establishment__specific_activity', RelatedDropdownFilter),
        ('establishment__plant_address__province', RelatedDropdownFilter),
        ('establishment__plant_address__municipality_or_city', RelatedDropdownFilter),
        ('job_type', ChoiceDropdownFilter),
        ('inspection_status', ChoiceDropdownFilter),
    )

    def name(self, job):
        return job.establishment.name

    def lto_number(self, job):
        return EstablishmentAdmin.lto_number(self, job.establishment)

    def expiry(self, job):
        return EstablishmentAdmin.expiry(self, job.establishment)

    def address(self, job):
        return EstablishmentAdmin.address(self, job.establishment)

    def product_type(self, job):
        return EstablishmentAdmin.product_type(self, job.establishment)

    def primary_activity(self, job):
        return EstablishmentAdmin.primary_activity(self, job.establishment)

    def specific_activity(self, job):
        return EstablishmentAdmin.specific_activities(self, job.establishment)

    def last_inspection(self, job):
        return EstablishmentAdmin.last_inspection(self, job.establishment)

    def mark_done(self, request, queryset):
        queryset.update(inspection_status=constants.INSPECTION_STATUS[0][0])
    mark_done.short_description = "Mark selected jobs as Complete"
