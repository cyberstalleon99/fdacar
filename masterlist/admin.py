from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.contrib import admin
from .models import Establishment, ProductType, PrimaryActivity, \
    AdditionalActivity, Region, Province, CityOrMunicipality, SpecificActivity, ProductLine, ProductType, \
    PlantAddress, WarehouseAddress, OfficeAddress, AuthorizedOfficer, QualifiedPerson, Lto, VariationType, \
    EstAdditionalActivity, EstProductLine, Variation

from records.models import Record
from checklist.models import Job
from django_reverse_admin import ReverseModelAdmin
from django.shortcuts import redirect
from datetime import datetime
from dateutil.relativedelta import relativedelta
from . import constants
from import_export.admin import ExportActionModelAdmin
from .myresources import EstablishmentResource
from tabbed_admin import TabbedModelAdmin
from nested_admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin

# @admin.register(Lto)
# class LtoAdmin(admin.ModelAdmin):


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



# class CapaPreparatorInline(admin.StackedInline):
#     model = CapaPreparator
#
# class CapaDeficiencyInline(admin.TabularInline):
#     model=CapaDeficiency
#     extra=1
#
# @admin.register(Capa)
# class CapaAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Start', {'fields': ['start_date']}),
#         ('End', {'fields': ['date_submitted', 'date_approved', 'approved_by', 'remarks']})
#     ]
#     inlines = [CapaPreparatorInline, CapaDeficiencyInline]

admin.site.register(AdditionalActivity)
admin.site.register(Region)
admin.site.register(SpecificActivity)
admin.site.register(PrimaryActivity)
admin.site.register(ProductLine)
admin.site.register(AuthorizedOfficer)
admin.site.register(QualifiedPerson)
admin.site.register(ProductType)
admin.site.register(OfficeAddress)
admin.site.register(PlantAddress)
admin.site.register(Variation)

class RecordInline(admin.StackedInline, NestedStackedInline):
    model = Record

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

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    inlines = [CityOrMunicipalityInline]

class WarehouseAddressInline(admin.TabularInline, NestedTabularInline):
    model=WarehouseAddress
    extra=1
    # insert_after = 'specific_activity'

class VariationInline(NestedTabularInline):
    model = Variation
    extra = 1

class LtoInline(NestedStackedInline):
    model = Lto
    extra = 1
    # classes = ['collapse']
    inlines = [VariationInline]

class QualifiedPersonInline(admin.TabularInline, NestedTabularInline):
    model=QualifiedPerson
    extra=1

@admin.register(Establishment)
# class EstablishmentAdmin(ExportActionModelAdmin, ReverseModelAdmin, TabbedModelAdmin):
class EstablishmentAdmin(NestedModelAdmin, ExportActionModelAdmin, TabbedModelAdmin):
    model = Establishment
    # fieldsets = [
    #     ('General Information', {'fields': ['status', 'name', 'center', 'product_type', 'primary_activity',
    #     'specific_activity'], 'classes': ['collapse']}),
    # ]

    list_display = ('name', 'plant_address', 'municipality_or_city', 'province',
     'product_type', 'primary_activity', 'specific_activities',
     'lto_number', 'expiry')

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

    tab_record = (
        RecordInline,
    )

    tabs = [
        ('General Information', tab_general_info),
        ('Address', tab_address),
        ('Personnel', tab_personnel),
        ('Applications', tab_applications),
        ('Records', tab_record),
    ]

    def province(self, obj):
        return obj.plant_address.province.name

    def municipality_or_city(self, obj):
        return obj.plant_address.municipality_or_city.name

    def lto_number(self, obj):
        return obj.ltos.first().lto_number

    def expiry(self, obj):
        return obj.ltos.first().expiry.date()

    def response_change(self, request, obj):
        return redirect('/admin/masterlist/establishment')
