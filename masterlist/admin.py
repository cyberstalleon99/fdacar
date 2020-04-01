from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.contrib import admin
from .models import Establishment, ProductType, PrimaryActivity, Person, \
    AdditionalActivity, Region, Province, CityOrMunicipality, SpecificActivity, ProductLine, \
    PlantAddress, WarehouseAddress, OfficeAddress, AuthorizedOfficer, QualifiedPerson, Inspection, Capa, CapaDeficiency, CapaPreparator, Lto

admin.site.register(Person)
admin.site.register(AdditionalActivity)
admin.site.register(Region)
admin.site.register(Province)
admin.site.register(CityOrMunicipality)
admin.site.register(SpecificActivity)
admin.site.register(PrimaryActivity)
admin.site.register(ProductLine)
admin.site.register(PlantAddress)
admin.site.register(WarehouseAddress)
admin.site.register(OfficeAddress)
admin.site.register(AuthorizedOfficer)
admin.site.register(QualifiedPerson)
admin.site.register(Inspection)

class CapaPreparatorInline(admin.StackedInline):
    model = CapaPreparator

class CapaDeficiencyInline(admin.TabularInline):
    model=CapaDeficiency
    extra=1

class CapaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Start', {'fields': ['start_date']}),
        ('End', {'fields': ['date_submitted', 'date_approved', 'approved_by', 'remarks']})
    ]
    inlines = [CapaPreparatorInline, CapaDeficiencyInline]

admin.site.register(Capa, CapaAdmin)

class PlantAddressInline(admin.StackedInline):
    model=PlantAddress

class OfficeAddressInline(PlantAddressInline):

    model=OfficeAddress

class WarehouseAddressInline(admin.TabularInline):
    model=WarehouseAddress
    extra=1

class LtoInline(admin.StackedInline):
    model=Lto

class AuthorizedOfficerInline(admin.StackedInline):
    model=AuthorizedOfficer

class QualifiedPersonInline(admin.TabularInline):
    model=QualifiedPerson
    extra=1

class EstablishmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General Information', {'fields': ['folder_id', 'status', 'application', 'name', 'center', 'product_type', 'primary_activity',
        'specific_activity', 'additional_activity', 'product_line', 'remarks']})
    ]

    list_display = ('name', 'plantaddress', 'municipality_or_city', 'province', 'product_type', 'primary_activity', 'specific_activities', 'additional_activity', 'product_line', 'remarks')
    list_filter = (
        ('name', DropdownFilter),
        ('product_type', RelatedDropdownFilter),
        ('primary_activity', RelatedDropdownFilter),
        ('specific_activity', RelatedDropdownFilter),
        ('plantaddress__province', RelatedDropdownFilter),
        ('plantaddress__municipality_or_city', RelatedDropdownFilter),
        ('status', ChoiceDropdownFilter),
    )

    inlines = [LtoInline, AuthorizedOfficerInline, QualifiedPersonInline, PlantAddressInline, WarehouseAddressInline, OfficeAddressInline]

    def province(self, obj):
        return obj.plantaddress.province.name

    def municipality_or_city(self, obj):
        return obj.plantaddress.municipality_or_city.name

admin.site.register(Establishment, EstablishmentAdmin)
