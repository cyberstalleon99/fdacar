from django.contrib import admin
from .models import Inspection, Capa, CapaDeficiency, CapaPreparator, Record, EstInspector, TypeOfInspection
from dateutil.relativedelta import relativedelta
from checklist.models import Job
from masterlist import constants
from nested_admin import NestedTabularInline, NestedModelAdmin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ExportActionModelAdmin
from .myresources import InspectionResource

admin.site.register(CapaPreparator)

@admin.register(TypeOfInspection)
class TypeOfInspectionAdmin(admin.ModelAdmin):
    model = TypeOfInspection
    list_display = ('id', 'name', 'short_name')

class InspectorInline(NestedTabularInline, admin.TabularInline):
    model = EstInspector
    extra = 1

@admin.register(Inspection)
class InspectionAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    inlines = (InspectorInline,)
    list_per_page = 20

    search_fields = ['record__establishment__name', 'tracking_number', 'record__establishment__ltos__lto_number']
    resource_class = InspectionResource

    list_display = ('name', 'address', 'product_type', 'primary_activity',
                    'specific_activities', 'lto_number', 'expiry', 'inspection_type', 'date_inspected',
                    'inspector', 'remarks',
    )

    list_filter = (
        ('est_inspectors__inspector', RelatedDropdownFilter),
        ('inspection_type', RelatedDropdownFilter),
        ('record__establishment__product_type', RelatedDropdownFilter),
        ('record__establishment__primary_activity', RelatedDropdownFilter),
        ('record__establishment__specific_activity', RelatedDropdownFilter),

    )

    fieldsets = [
        (
            'General Information',
            {'fields': ['record', 'tracking_number', 'inspection_type', 'date_inspected']}
        ),
        (
            'Risk Rating',
            {'fields': ['frequency_of_inspection', 'risk_rating']}
        ),
        (
            'CAPA',
            {'fields': ['capa']}
        ),
        (
            'Notes on Inspection',
            {'fields': ['remarks']}
        ),
        (
            'Inspection Report',
            {'fields': ['inspection_report']}
        ),
        (
            'CAPA Status',
            {'fields': ['for_capa']}
        ),
        (
            'Forwarded to supervisor',
            {'fields': ['date_forwarded', 'date_approved']}
        ),
    ]

    def name(self, inspection):
        return inspection.record.establishment.name

    def address(self, inspection):
        return inspection.record.establishment.plant_address.full_address()

    def product_type(self, inspection):
        return inspection.record.establishment.product_type

    def primary_activity(self, inspection):
        return inspection.record.establishment.primary_activity.name

    def specific_activities(self, inspection):
        return inspection.record.establishment.specific_activities()

    def lto_number(self, inspection):
        try:
            inspection.record.establishment.ltos.first().lto_number
        except:
            return "N/A"
        else:
            return inspection.record.establishment.ltos.first().lto_number

    def expiry(self, inspection):
        try:
            inspection.record.establishment.ltos.first().expiry
        except:
            return "N/A"
        else:
            return inspection.record.establishment.ltos.first().expiry

    def inspection_type(self, inspection):
        return inspection.inspection_type

    def date_inspected(self, inspection):
        return inspection.date_inspected

    def inspector(self, inspection):
        return ",\n".join(inspector.inspector.get_short_name()  for inspector in inspection.est_inspectors.all())

    def remarks(self, inspection):
        return inspection.remarks

class InspectionInline(NestedTabularInline, admin.TabularInline):
    model = Inspection
    extra = 1
    exclude = ['date_of_followup_inspection']
    inlines = [InspectorInline]

    def save_formset(self, request, form, formset, change):
        # if it's not the model we want to change
        # just call the default function
        if formset.model != Inspection:
            return super(RecordAdmin, self).save_formset(request, form, formset, change)

        # if it is, do our custom stuff
        instances = formset.save(commit=False)
        for instance in instances:
            frequency_of_inspection = request.POST.get('frequency_of_inspection')
            date_inspec = request.POST.get('date_inspected')
            form.date_of_followup_inspection = date_inspec + relativedelta(years=int(frequency_of_inspection))
            instance.save()
            est = form.record.establishment
            if Job.objects.filter(establishment=est).exists():
                curr_job = Job.objects.get(establishment=est)
                # Set the Job object's inspection status to 'inspected'
                curr_job.inspection_status = constants.INSPECTION_STATUS[0]
                curr_job.save()



@admin.register(Record)
class RecordAdmin(NestedModelAdmin):
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
