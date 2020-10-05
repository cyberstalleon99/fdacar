from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from dateutil.relativedelta import relativedelta
from django.contrib import admin
from .models import Establishment, CityOrMunicipality, \
    PlantAddress, WarehouseAddress, OfficeAddress, AuthorizedOfficer, QualifiedPerson, Lto, VariationType, \
    EstAdditionalActivity, EstProductLine, Variation, SpecificActivity, QualifiedPersonDesignation

# from records.models import Record
# from checklist.models import Job
# from django_reverse_admin import ReverseModelAdmin
from django.shortcuts import redirect
from import_export.admin import ExportActionModelAdmin
from .myresources import EstablishmentResource
from tabbed_admin import TabbedModelAdmin
from nested_admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin

# @admin.register(Inspection)
# class InspectionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('General Information', {'fields': ['establishment', 'tracking_number', 'type_of_inspection', 'date_inspected', 'inspector', 'remarks']}),
#         ('Risk Rating', {'fields': ['frequency_of_inspection', 'risk_rating']}),
#         ('CAPA', {'fields': ['capa']}),
#         ('Inspection Report', {'fields': ['inspection_report']}),
#     ]
#
#     def save_model(self, request, obj, form, change):
#         frequency_of_inspection = request.POST.get('frequency_of_inspection')
#         date_inspec = request.POST.get('date_inspected_0')
#         time_inspec = request.POST.get('date_inspected_1')
#
#         date_time_inspected = datetime.strptime(date_inspec + ' ' + time_inspec, '%Y-%m-%d %H:%M:%S')
#         obj.date_of_followup_inspection = date_time_inspected + relativedelta(years=int(frequency_of_inspection))
#
#         est = obj.establishment
#         if Job.objects.filter(establishment=est).exists():
#             curr_job = Job.objects.get(establishment=est)
#             # Set the Job object's inspection status to 'inspected'
#             curr_job.inspection_status = constants.INSPECTION_STATUS[0]
#             curr_job.save()
#
#         return super().save_model(request, obj, form, change)

admin.site.register(AuthorizedOfficer)
admin.site.register(QualifiedPerson)
admin.site.register(OfficeAddress)
admin.site.register(PlantAddress)
admin.site.register(Variation)
admin.site.register(SpecificActivity)
admin.site.register(QualifiedPersonDesignation)


@admin.register(VariationType)
class VariationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')

class AdditionalActivityInline(admin.TabularInline, NestedStackedInline):
    model = EstAdditionalActivity
    extra = 1
    # insert_after = 'specific_activity'

class ProductLineInline(admin.TabularInline, NestedTabularInline):
    model = EstProductLine
    extra = 1
    # insert_after = 'specific_activity'

class CityOrMunicipalityInline(admin.TabularInline, NestedTabularInline):
    model=CityOrMunicipality
    extra=5

class WarehouseAddressInline(admin.TabularInline, NestedTabularInline):
    model=WarehouseAddress
    extra=1
    # insert_after = 'specific_activity'

class VariationInline(NestedTabularInline, admin.TabularInline):
    model = Variation
    extra = 2

class LtoInline(NestedStackedInline, admin.StackedInline):
    model = Lto
    extra = 3
    # classes = ['collapse']
    inlines = [VariationInline]

class QualifiedPersonInline(admin.TabularInline, NestedTabularInline):
    model=QualifiedPerson
    extra=1

@admin.register(Establishment)
# class EstablishmentAdmin(ExportActionModelAdmin, ReverseModelAdmin, TabbedModelAdmin):
class EstablishmentAdmin(NestedModelAdmin, ExportActionModelAdmin, TabbedModelAdmin):
    model = Establishment
    list_per_page = 20
    except_activities = ['Medical X-Ray', 'Veterinary X-Ray', 'Dental X-Ray', 'Educational X-Ray', 'MRI', 'CTScan']
    # fieldsets = [
    #     ('General Information', {'fields': ['status', 'name', 'center', 'product_type', 'primary_activity',
    #     'specific_activities'], 'classes': ['collapse']}),
    # ]

    search_fields = ['name']

    list_display = ('name', 'address',
     'product_type', 'primary_activity', 'specific_activities',
     'lto_number', 'expiry',
     'last_inspection', 'next_inspection', 'type_of_inspection', 'folder')

    list_filter = (
        ('name', DropdownFilter),
        ('product_type', RelatedDropdownFilter),
        ('primary_activity', RelatedDropdownFilter),
        ('specific_activity', RelatedDropdownFilter),
        ('plant_address__province', RelatedDropdownFilter),
        ('plant_address__municipality_or_city', RelatedDropdownFilter),
        ('status', ChoiceDropdownFilter),
    )
    #
    # inlines = [QualifiedPersonInline, AdditionalActivityInline, ProductLineInline, WarehouseAddressInline, LtoInline]
    #
    # inline_type = 'stacked'
    # inline_reverse = ['office_address', 'plant_address', 'authorized_officer']
    # change_form_template = 'admin/custom/change_form.html'
    resource_class = EstablishmentResource

    test = ('General Information', {'fields': ['status', 'name', 'center', 'product_type', 'primary_activity',
            'specific_activity']})

    tab_general_info = (
        ('General Information', {'fields': ['status', 'name', 'center', 'product_type', 'primary_activity',
            'specific_activity']}),
        AdditionalActivityInline,
        ProductLineInline
    )

    tab_address = (
        ('Office Address', {'fields': ['office_address']}),
        ('Plant Address',  {'fields': ['plant_address']}),
        WarehouseAddressInline
    )

    tab_personnel = (
        ('Authorized Officer', {'fields': ['authorized_officer']}),
        QualifiedPersonInline
    )

    tab_applications = (
        LtoInline,
    )

    tabs = [
        ('General Information', tab_general_info),
        ('Applications', tab_applications),
        ('Address', tab_address),
        ('Personnel', tab_personnel),

        # ('Records', tab_record),
    ]

    def folder(self, obj):
        return obj.record.folder_id

    def product_type(self, obj):
        return obj.product_type.name

    def primary_activity(self, obj):
        return obj.primary_activity.name

    def specific_activities(self, obj):
        return obj.specific_activities()

    def address(self, obj):
        return obj.plant_address.full_address()

    def lto_number(self, obj):
        try:
            obj.ltos.first().lto_number
        except:
            return "N/A"
        else:
            return obj.ltos.first().lto_number

    def expiry(self, obj):
        try:
            obj.ltos.first().expiry
        except:
            return "N/A"
        else:
            return obj.ltos.first().expiry

    def response_change(self, request, obj):
        return redirect('/admin/masterlist/establishment')

    def last_inspection(self, obj):
        if obj.specific_activity.filter(name__in=self.except_activities).exists()==False:
            return obj.record.inspections.latest().date_inspected
        else:
            return 'N/A'

    def next_inspection(self, obj):
        next_date_inspection = ''
        if obj.specific_activity.filter(name__in=self.except_activities).exists()==False:
            try:
                obj.record.inspections.latest()
            except:
                return 'For inspection'
            else:
                frequency_of_inspection = obj.record.inspections.latest().frequency_of_inspection
                if frequency_of_inspection:
                    next_date_inspection = obj.record.inspections.latest().date_inspected + relativedelta(years=int(frequency_of_inspection))
                else:
                    return 'No Risk Assessment'
            return next_date_inspection
        else:
            return 'N/A'

    def type_of_inspection(self, obj):
        if obj.specific_activity.filter(name__in=self.except_activities).exists()==False:
            return obj.record.inspections.latest().inspection_type
        else:
            return 'N/A'

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
