from django.contrib import admin
from .models import Application
from dateutil.relativedelta import relativedelta
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from import_export.admin import ExportActionModelAdmin
from .myresources import ApplicationResource

@admin.register(Application)
class ApplicationAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    model = Application
    list_per_page = 20
    list_display = (
        'status', 'tracking_number', 'month', 'name', 'address', 'product_type',
        'primary_activity', 'specific_activity', 'lto_number', 'expiry', 'application_type',
        'type_of_variation', 'payment', 'date_received_by_rfo', 'date_received_by_inspector',
        'inspector', 'date_inspected', 'notes_on_inspection', 'date_accomplished', 'capa_start_date', 'capa_date_received',
        'capa_processing_duration', 'recommendation', 'date_approved_by_supervisor', 'processing_duration',
        'eod_no_inspection', 'eod_with_inspection', 'backlog', 'reason',
    )

    search_fields = ['establishment__name', 'tracking_number']
    list_filter = (
        ('establishment__name', DropdownFilter),
        ('establishment__product_type', RelatedDropdownFilter),
        ('establishment__primary_activity', RelatedDropdownFilter),
        ('establishment__specific_activity', RelatedDropdownFilter),
        ('establishment__plant_address__province', RelatedDropdownFilter),
        ('establishment__plant_address__municipality_or_city', RelatedDropdownFilter),
        ('inspection__inspector', RelatedDropdownFilter),
        ('status', DropdownFilter),
        ('applied_thru', DropdownFilter),
        ('group', DropdownFilter),
        ('application_type', DropdownFilter),
    )

    resource_class = ApplicationResource


    def month(self, pli):
        return pli.group.strftime('%B')

    def product_type(self, application):
        return application.establishment.product_type.name

    def name(self, application):
        return application.establishment.name

    def address(self, application):
        return application.establishment.plant_address.full_address()

    def primary_activity(self, application):
        return application.establishment.primary_activity.name

    def specific_activity(self, application):
        return application.establishment.specific_activities()

    def lto_number(self, application):
        return application.establishment.ltos.first().lto_number

    def expiry(self, application):
        return application.establishment.ltos.first().expiry

    def inspector(self, application):
        return application.inspection.inspector.get_short_name()

    def date_inspected(self, application):
        return application.inspection.date_inspected

    def notes_on_inspection(self, application):
        return application.inspection.remarks

    def capa_start_date(self, application):
        try:
            application.inspection.capa.date_prepared
        except:
            return None
        else:
            return application.inspection.capa.date_prepared

    def capa_date_received(self, application):
        try:
            application.inspection.capa.date_submitted
        except:
            return None
        else:
            return application.inspection.capa.date_submitted

    def capa_processing_duration(self, application):
        try:
            application.inspection.capa.date_prepared
            application.inspection.capa.date_submitted
        except:
            return None
        else:
            start_date = application.inspection.capa.date_prepared
            end_date = application.inspection.capa.date_submitted
            difference = relativedelta(end_date, start_date)
            return difference

    def eod_no_inspection(self, application):
        return application.eod_1

    def eod_with_inspection(self, application):
        return application.eod_2

    def reason(self, application):
        return application.reason_1

