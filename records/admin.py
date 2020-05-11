from django.contrib import admin
from .models import Inspection, Capa, CapaDeficiency, CapaPreparator, Record
from datetime import datetime
from dateutil.relativedelta import relativedelta
from checklist.models import Job

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('folder_id', 'name', 'address', 'province', 'municipality_or_city', )

    def name(self, obj):
        return obj.establishment.name

    def address(self, obj):
        return obj.establishment.plant_address.address

    def province(self, obj):
        return obj.establishment.plant_address.province.name

    def municipality_or_city(self, obj):
        return obj.establishment.plant_address.municipality_or_city.name

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General Information', {'fields': ['record', 'tracking_number', 'type_of_inspection', 'date_inspected', 'inspector', 'remarks']}),
        ('Risk Rating', {'fields': ['frequency_of_inspection', 'risk_rating']}),
        ('CAPA', {'fields': ['capa']}),
        ('Inspection Report', {'fields': ['inspection_report']}),
    ]

    def save_model(self, request, obj, form, change):
        frequency_of_inspection = request.POST.get('frequency_of_inspection')
        date_inspec = request.POST.get('date_inspected_0')
        time_inspec = request.POST.get('date_inspected_1')

        date_time_inspected = datetime.strptime(date_inspec + ' ' + time_inspec, '%Y-%m-%d %H:%M:%S')
        obj.date_of_followup_inspection = date_time_inspected + relativedelta(years=int(frequency_of_inspection))

        est = obj.record.establishment
        if Job.objects.filter(establishment=est).exists():
            curr_job = Job.objects.get(establishment=est)
            # Set the Job object's inspection status to 'inspected'
            curr_job.inspection_status = constants.INSPECTION_STATUS[0]
            curr_job.save()

        return super().save_model(request, obj, form, change)

class CapaPreparatorInline(admin.StackedInline):
    model = CapaPreparator

class CapaDeficiencyInline(admin.TabularInline):
    model=CapaDeficiency
    extra=1

@admin.register(Capa)
class CapaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Start', {'fields': ['start_date']}),
        ('End', {'fields': ['date_submitted', 'date_approved', 'approved_by', 'remarks']})
    ]

    inlines = [CapaPreparatorInline, CapaDeficiencyInline]
