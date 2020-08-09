from django.contrib import admin
from .models import Pli, PliStatus
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from import_export.admin import ExportActionModelAdmin
from .myresources import PliResource

admin.site.register(PliStatus)
# admin.site.register(Pli)

@admin.register(Pli)
class PliAdmin(ExportActionModelAdmin, admin.ModelAdmin):
        model = Pli
        list_per_page = 20
        ordering = ('-group',)

        list_display = ('status', 'name', 'address', 'month', 'product_type', 'primary_activity',
                        'specific_activities', 'lto_number', 'expiry', 'type_of_inspection', 'date_inspected',
                        'inspector', 'remarks',
        )

        list_filter = (
            ('inspection__inspector', RelatedDropdownFilter),
            ('inspection__type_of_inspection', DropdownFilter),
            ('inspection__record__establishment__product_type', RelatedDropdownFilter),
            ('inspection__record__establishment__primary_activity', RelatedDropdownFilter),
            ('inspection__record__establishment__specific_activity', RelatedDropdownFilter),
            ('status', RelatedDropdownFilter),
            ('group', DropdownFilter),

        )

        search_fields = ['inspection__record__establishment__name']
        resource_class = PliResource

        def name(self, pli):
            return pli.inspection.record.establishment.name

        def address(self, pli):
            return pli.inspection.record.establishment.plant_address.full_address()

        def month(self, pli):
            return pli.group.strftime('%B')

        def product_type(self, pli):
            return pli.inspection.record.establishment.product_type

        def primary_activity(self, pli):
            return pli.inspection.record.establishment.primary_activity.name

        def specific_activities(self, pli):
            return pli.inspection.record.establishment.specific_activities()

        def lto_number(self, pli):
            return pli.inspection.record.establishment.ltos.first().lto_number

        def expiry(self, pli):
            return pli.inspection.record.establishment.ltos.first().expiry

        def type_of_inspection(self, pli):
            return pli.inspection.type_of_inspection

        def date_inspected(self, pli):
            return pli.inspection.date_inspected

        def inspector(self, pli):
            return pli.inspection.inspector

        def remarks(self, pli):
            return pli.inspection.remarks

