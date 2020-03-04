from django.contrib import admin
from .models import Establishment, ProductType, PrimaryActivity, Person, \
    AdditionalActivity, Region, Province, CityOrMunicipality, SpecificActivity, ProductLine, \
    PlantAddress, WarehouseAddress, OfficeAddress, AuthorizedOfficer, Inspection

# admin.site.register(ProductType)
admin.site.register(Establishment)
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
admin.site.register(Inspection)
# class EstablishmentAdmin(admin.ModelAdmin):
#     # fieldsets = [
#     #     ('LTO Information', {'fields': ['lto'], 'classes': ['collapse']}),
#     # ]
#     # inlines = []
#     raw_id_fields = ("plant_address", "warehouse_address")
#
# admin.site.register(Establishment, EstablishmentAdmin)

# class PrimaryActivityInline(admin.TabularInline):
#     model = PrimaryActivity
#     extra = 3
#
# class SpecificActivityInline(admin.TabularInline):
#     model = SpecificActivity
#     extra = 3
#
# class ProductTypeAdmin(admin.ModelAdmin):
#     inlines = [PrimaryActivityInline, SpecificActivityInline]
#
# admin.site.register(ProductType, ProductTypeAdmin)

