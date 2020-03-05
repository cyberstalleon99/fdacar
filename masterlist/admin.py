from django.contrib import admin
from .models import Establishment, ProductType, PrimaryActivity, Person, \
    AdditionalActivity, Region, Province, CityOrMunicipality, SpecificActivity, ProductLine, \
    PlantAddress, WarehouseAddress, OfficeAddress, AuthorizedOfficer, QualifiedPerson, Inspection, Capa, CapaDeficiency, CapaPreparator, Lto

# admin.site.register(ProductType)
# admin.site.register(Establishment)
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
admin.site.register(CapaPreparator)

class CapaDeficiencyInline(admin.TabularInline):
    model=CapaDeficiency
    extra=3

class CapaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Start', {'fields': ['start_date', 'prepared_by']}),
        ('End', {'fields': ['date_submitted', 'date_approved', 'approved_by', 'remarks']})
    ]
    inlines = [CapaDeficiencyInline]

admin.site.register(Capa, CapaAdmin)

class LtoInline(admin.StackedInline):
    model=Lto

class AuthorizedOfficerInline(admin.StackedInline):
    model=AuthorizedOfficer

class QualifiedPersonInline(admin.TabularInline):
    model=QualifiedPerson
    extra=2

class EstablishmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General Information', {'fields': ['application', 'name', 'center', 'product_type', 'primary_activity',
        'specific_activity', 'additional_activity', 'product_line', 'remarks']})
    ]

    inlines = [LtoInline, AuthorizedOfficerInline, QualifiedPersonInline]

admin.site.register(Establishment, EstablishmentAdmin)
