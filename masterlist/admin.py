from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from dateutil.relativedelta import relativedelta
from django.contrib import admin
from .models import Establishment, CityOrMunicipality, \
    PlantAddress, WarehouseAddress, OfficeAddress, AuthorizedOfficer, QualifiedPerson, Lto, VariationType, \
    EstAdditionalActivity, EstProductLine, Variation, SpecificActivity, QualifiedPersonDesignation, QualifiedPerson, ProductType

# from records.models import Record
# from checklist.models import Job
# from django_reverse_admin import ReverseModelAdmin
from django.shortcuts import redirect
from import_export.admin import ExportActionModelAdmin
from .myresources import EstablishmentResource, LtoResource, QualifiedPersonResource
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
# admin.site.register(QualifiedPerson)
admin.site.register(OfficeAddress)
admin.site.register(PlantAddress)
admin.site.register(Variation)
admin.site.register(SpecificActivity)
admin.site.register(QualifiedPersonDesignation)

@admin.register(Lto)
class LtoAdmin(ExportActionModelAdmin):
    model = Lto
    # list_display = ('LTO #', 'Type', 'Date Issued', 'Expiry', 'Establishment',
    # 'Address', 'City or Municip', 'Primary Activity', 'Specific Activity',  'Inspections',)

    list_display = ('lto_number', 'type_of_application', 'issuance', 'expiry',
    'name', 'address', 'city_or_municipality', 'province', 'primary_activity', 'specific_activity',
    'inspections', 'status', 'folder_number')

    list_filter = (
        ('type_of_application', DropdownFilter),
        ('establishment__record__inspections__inspection_type', RelatedDropdownFilter),
        ('establishment__primary_activity', RelatedDropdownFilter),
        ('establishment__specific_activity', RelatedDropdownFilter),
        ('establishment__plant_address__province', RelatedDropdownFilter),
        ('establishment__plant_address__municipality_or_city', RelatedDropdownFilter),
    )

    search_fields = ['establishment__name', 'establishment__ltos__lto_number']

    resource_class = LtoResource

    def name(self, lto):
        return lto.establishment.name

    def address(self, lto):
        return lto.establishment.plant_address.address

    def city_or_municipality(self, lto):
        return lto.establishment.plant_address.municipality_or_city

    def province(self, lto):
        return lto.establishment.plant_address.province.name

    def primary_activity(self, lto):
        return lto.establishment.primary_activity.name

    def specific_activity(self, lto):
         return lto.establishment.specific_activities()

    def inspections(self, lto):
        try:
            lto.establishment.record.inspections.all()
        except:
            return 'No inspections'
        else:
            inspections = lto.establishment.record.inspections.all()
            return ", \n".join(s.date_inspected.strftime('%d %b %Y') + ' - ' + s.inspection_type.name for s in inspections)

    def status(self, lto):
        return lto.establishment.status

    def folder_number(self, lto):
        try:
            lto.establishment.record.inspections.all()
        except:
            return 'No Folder'
        else:
            return lto.establishment.record.folder_id



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

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    search_fields  = ["name"]

@admin.register(Establishment)
# class EstablishmentAdmin(ExportActionModelAdmin, ReverseModelAdmin, TabbedModelAdmin):
class EstablishmentAdmin(NestedModelAdmin, ExportActionModelAdmin, TabbedModelAdmin):
    model = Establishment
    # search_fields   = ["product_type", ]
    autocomplete_fields  = ["product_type", ]
    list_per_page = 20
    except_activities = ['Medical X-Ray', 'Veterinary X-Ray', 'Dental X-Ray', 'Educational X-Ray', 'MRI', 'CTScan']
    # fieldsets = [
    #     ('General Information', {'fields': ['status', 'name', 'center', 'product_type', 'primary_activity',
    #     'specific_activities'], 'classes': ['collapse']}),
    # ]

    search_fields = ['name', 'ltos__lto_number']

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

    def folder(self, establishment):
        return establishment.record.folder_id

    def product_type(self, establishment):
        return establishment.product_type.name

    def primary_activity(self, establishment):
        return establishment.primary_activity.name

    def specific_activities(self, establishment):
        return establishment.specific_activities()

    def address(self, establishment):
        return establishment.plant_address.full_address()

    def lto_number(self, establishment):
        try:
            establishment.ltos.first().lto_number
        except:
            return "N/A"
        else:
            return establishment.ltos.first().lto_number

    def expiry(self, establishment):
        try:
            establishment.ltos.first().expiry
        except:
            return "N/A"
        else:
            return establishment.ltos.first().expiry

    def response_change(self, request, establishment):
        return redirect('/admin/masterlist/establishment')

    def last_inspection(self, establishment):
        if establishment.specific_activity.filter(name__in=self.except_activities).exists()==False:
            return establishment.record.inspections.latest().date_inspected
        else:
            return 'N/A'

    def next_inspection(self, establishment):
        next_date_inspection = ''
        if establishment.specific_activity.filter(name__in=self.except_activities).exists()==False:
            try:
                establishment.record.inspections.latest()
            except:
                return 'For inspection'
            else:
                frequency_of_inspection = establishment.record.inspections.latest().frequency_of_inspection
                if frequency_of_inspection:
                    next_date_inspection = establishment.record.inspections.latest().date_inspected + relativedelta(years=int(frequency_of_inspection))
                else:
                    return 'No Risk Assessment'
            return next_date_inspection
        else:
            return 'N/A'

    def type_of_inspection(self, establishment):
        if establishment.specific_activity.filter(name__in=self.except_activities).exists()==False:
            return establishment.record.inspections.latest().inspection_type
        else:
            return 'N/A'

    def has_delete_permission(self, request, establishment=None):
        return False

    def save_model(self, request, establishment, form, change):
        establishment.modified_by = request.user
        super().save_model(request, establishment, form, change)

@admin.register(QualifiedPerson)
class QualifiedPersonAdmin(ExportActionModelAdmin):
    list_display = ('status', 'name', 'establishment', 'lto_number', 'address',
    'primary_activity', 'specific_activities', 'designation')
    list_filter = (
        ('status', DropdownFilter),
        ('designation', RelatedDropdownFilter),
        ('establishment__product_type', RelatedDropdownFilter),
        ('establishment__primary_activity', RelatedDropdownFilter),
        ('establishment__specific_activity', RelatedDropdownFilter),
        ('establishment__status', DropdownFilter),
    )
    resource_class = QualifiedPersonResource
    list_per_page = 20
    search_fields = ['first_name', 'last_name', 'establishment__name']

    def name(self, person):
        return person.full_name()

    def primary_activity(self, person):
        try:
            person.establishment.primary_activity
        except:
            return 'Does not belong to an establishment'
        else:
            return person.establishment.primary_activity

    def specific_activities(self, person):

        try:
            person.establishment.specific_activities()
        except:
            return 'Does not belong to an establishment'
        else:
            return person.establishment.specific_activities()

    def lto_number(self, person):
        try:
            person.establishment.ltos.latest()
        except:
            return 'No LTO Number'
        else:
            return person.establishment.ltos.latest()

    def address(self, person):
        try:
            person.establishment.plant_address.full_address()
        except:
            return 'Does not belong to an establishment'
        else:
            return person.establishment.plant_address.full_address()
