from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from import_export.admin import ExportActionModelAdmin
from .myresources import OutgoinResource

from .models import Outgoing, Courier

admin.site.register(Courier)

@admin.register(Outgoing)
class OutgoinAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    model = Outgoing
    resource_class = OutgoinResource
    list_display = (
        'month', 'tracking_number', 'document_type', 'particulars', 'remarks',
        'courier', 'courier_tracking_number', 'date_forwarded', 'forwarded_by',
        'forwarded_to', 'forwarded_to_1',
    )

    list_filter = (
        ('group', DropdownFilter),
        ('document_type', RelatedDropdownFilter),
        ('courier', RelatedDropdownFilter),
        ('forwarded_to', DropdownFilter),
        ('forwarded_to_1', DropdownFilter),
    )

    search_fields = ['tracking_number', 'particulars', 'remarks', 'courier__name', 'courier_tracking_number',
    'forwarded_to', 'forwarded_to_1']

    def month(self, outgoing):
        return outgoing.group.strftime('%B')

    def document_type(self, outgoing):
        return outgoing.document_type.name

    def courier(self, outgoing):
        return outgoing.courier.name

    def forwarded_by(self, outgoing):
        return outgoing.forwarded_by.get_short_name()