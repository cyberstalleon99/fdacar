from django.contrib import admin
from .models import Inspection, Capa, CapaDeficiency, CapaPreparator, Record
from datetime import datetime
from dateutil.relativedelta import relativedelta
from checklist.models import Job
from masterlist import constants

admin.site.register(CapaPreparator)
admin.site.register(Inspection)

class InspectionInline(admin.TabularInline):
    model = Inspection
    extra = 1
    exclude = ['date_of_followup_inspection']

    def save_formset(self, request, form, formset, change):
        # if it's not the model we want to change
        # just call the default function
        if formset.model != Inspection:
            return super(RecordAdmin, self).save_formset(request, form, formset, change)

        # if it is, do our custom stuff
        instances = formset.save(commit=False)
        for instance in instances:
            frequency_of_inspection = request.POST.get('frequency_of_inspection')
            # date_inspec = request.POST.get('date_inspected_0')
            date_inspec = request.POST.get('date_inspected')
            # time_inspec = request.POST.get('date_inspected_1')

            # date_time_inspected = datetime.strptime(date_inspec + ' ' + time_inspec, '%Y-%m-%d %H:%M:%S')
            # form.date_of_followup_inspection = date_time_inspected + relativedelta(years=int(frequency_of_inspection))
            form.date_of_followup_inspection = date_inspec + relativedelta(years=int(frequency_of_inspection))

            est = form.record.establishment
            if Job.objects.filter(establishment=est).exists():
                curr_job = Job.objects.get(establishment=est)
                # Set the Job object's inspection status to 'inspected'
                curr_job.inspection_status = constants.INSPECTION_STATUS[0]
                curr_job.save()

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('folder_id', 'name', 'address', 'province', 'municipality_or_city', )
    inlines = [InspectionInline]

    def name(self, obj):
        return obj.establishment.name

    def address(self, obj):
        return obj.establishment.plant_address.address

    def province(self, obj):
        return obj.establishment.plant_address.province.name

    def municipality_or_city(self, obj):
        return obj.establishment.plant_address.municipality_or_city.name

# @admin.register(Inspection)
# class InspectionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('General Information', {'fields': ['record', 'tracking_number', 'type_of_inspection', 'date_inspected', 'inspector', 'remarks']}),
#         ('Risk Rating', {'fields': ['frequency_of_inspection', 'risk_rating']}),
#         ('CAPA', {'fields': ['capa']}),
#         ('Inspection Report', {'fields': ['inspection_report']}),
#     ]

#     def save_model(self, request, obj, form, change):
#         frequency_of_inspection = request.POST.get('frequency_of_inspection')
#         date_inspec = request.POST.get('date_inspected_0')
#         time_inspec = request.POST.get('date_inspected_1')

#         date_time_inspected = datetime.strptime(date_inspec + ' ' + time_inspec, '%Y-%m-%d %H:%M:%S')
#         obj.date_of_followup_inspection = date_time_inspected + relativedelta(years=int(frequency_of_inspection))

#         est = obj.record.establishment
#         if Job.objects.filter(establishment=est).exists():
#             curr_job = Job.objects.get(establishment=est)
#             # Set the Job object's inspection status to 'inspected'
#             curr_job.inspection_status = constants.INSPECTION_STATUS[0]
#             curr_job.save()

#         return super().save_model(request, obj, form, change)

# class CapaPreparatorInline(admin.StackedInline):
#     model = CapaPreparator

class CapaDeficiencyInline(admin.TabularInline):
    model=CapaDeficiency
    extra=1
    line_numbering = 0
    fields = ('line_number', 'type', 'capa', 'description', 'action', 'evidence', 'proposed_completion_date', 'inspector_comment', 'accepted')
    readonly_fields = ('line_number',)

    def line_number(self, obj):
        self.line_numbering += 1
        return self.line_numbering

    line_number.short_description = '#'
    # proposed_comletion_date = models.DateField(verbose_name="Proposed Completion Date")
    # inspector_comment = models.CharField(max_length=200, blank=True)
    # accepted = models.BooleanField(default=False)

@admin.register(Capa)
class CapaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Start', {'fields': ['date_submitted', 'date_prepared', 'prepared_by']}),
        ('End', {'fields': ['date_approved', 'approved_by', 'remarks', 'recommendation']})
    ]

    inlines = [CapaDeficiencyInline,]
