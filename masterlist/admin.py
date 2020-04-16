from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.contrib import admin
from .models import Establishment, ProductType, PrimaryActivity, Person, \
    AdditionalActivity, Region, Province, CityOrMunicipality, SpecificActivity, ProductLine, ProductType, \
    PlantAddress, WarehouseAddress, OfficeAddress, AuthorizedOfficer, QualifiedPerson, Inspection, Capa, CapaDeficiency, CapaPreparator, Lto
from checklist.models import Job
from django_reverse_admin import ReverseModelAdmin
from django.shortcuts import redirect
from datetime import datetime
from dateutil.relativedelta import relativedelta
from . import constants

admin.site.register(Person)
admin.site.register(AdditionalActivity)
admin.site.register(Region)
admin.site.register(SpecificActivity)
admin.site.register(PrimaryActivity)
admin.site.register(ProductLine)
admin.site.register(AuthorizedOfficer)
admin.site.register(QualifiedPerson)
admin.site.register(ProductType)

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General Information', {'fields': ['establishment', 'tracking_number', 'type_of_inspection', 'date_inspected', 'inspector', 'remarks']}),
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

        est = obj.establishment
        print('Outside if...................')
        if Job.objects.filter(establishment=est).exists():
            print('Inside if...................')
            curr_job = Job.objects.get(establishment=est)
            # Set the Job object's inspection status to 'inspected'
            curr_job.inspection_status = constants.INSPECTION_STATUS[0]
            curr_job.save()

        return super().save_model(request, obj, form, change)

class CityOrMunicipalityInline(admin.TabularInline):
    model=CityOrMunicipality
    extra=5

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    inlines = [CityOrMunicipalityInline]

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

class WarehouseAddressInline(admin.TabularInline):
    model=WarehouseAddress
    extra=1

class LtoInline(admin.StackedInline):
    model=Lto
    extra=1

class QualifiedPersonInline(admin.TabularInline):
    model=QualifiedPerson
    extra=1

@admin.register(Establishment)
class EstablishmentAdmin(ReverseModelAdmin):
    fieldsets = [
        ('General Information', {'fields': ['folder_id', 'status', 'application', 'name', 'center', 'product_type', 'primary_activity',
        'specific_activity', 'additional_activity', 'product_line', 'remarks']})
    ]

    list_display = ('name', 'plant_address', 'municipality_or_city', 'province',
     'product_type', 'primary_activity', 'specific_activities', 'additional_activity', 'product_line', 'remarks',
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

    inlines = [QualifiedPersonInline, WarehouseAddressInline, LtoInline]

    inline_type = 'stacked'
    inline_reverse = ['office_address', 'plant_address', 'authorized_officer']

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
