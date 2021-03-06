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

        list_display = ('status', 'dtn', 'name', 'address', 'month', 'product_type', 'primary_activity',
                        'specific_activities', 'lto_number', 'expiry', 'inspection_type', 'date_inspected', 'inspection_count',
                        'inspector', 'remarks',
        )

        list_filter = (
            ('inspection__est_inspectors__inspector', RelatedDropdownFilter),
            ('inspection__inspection_type', RelatedDropdownFilter),
            ('inspection__record__establishment__product_type', RelatedDropdownFilter),
            ('inspection__record__establishment__primary_activity', RelatedDropdownFilter),
            ('inspection__record__establishment__specific_activity', RelatedDropdownFilter),
            ('status', RelatedDropdownFilter),
            ('group', DropdownFilter),

        )

        search_fields = ['inspection__record__establishment__name', 'inspection__tracking_number', 'inspection__record__establishment__ltos__lto_number']
        autocomplete_fields = ['inspection']
        resource_class = PliResource

        def name(self, pli):
            return pli.inspection.record.establishment.name

        def dtn(self, pli):
            return pli.inspection.tracking_number

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
            try:
                pli.inspection.record.establishment.ltos.first().lto_number
            except:
                return "N/A"
            else:
                return pli.inspection.record.establishment.ltos.first().lto_number

        def expiry(self, pli):
            try:
                pli.inspection.record.establishment.ltos.first().expiry
            except:
                return "N/A"
            else:
                return pli.inspection.record.establishment.ltos.first().expiry

        def inspection_type(self, pli):
            return pli.inspection.inspection_type

        def date_inspected(self, pli):
            return pli.inspection.date_inspected

        def inspection_count(self, pli):
            record = pli.inspection.record
            count = record.inspections.count()
            return count

        def inspector(self, pli):
            return ",\n".join(inspector.inspector.get_short_name()  for inspector in pli.inspection.est_inspectors.all())

        def remarks(self, pli):
            return pli.inspection.remarks

