from django.contrib import admin
from .models import Incoming, DocumentType
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from import_export.admin import ExportActionModelAdmin
from .myresources import IncomingResource

# admin.site.register(Incoming)
admin.site.register(DocumentType)


@admin.register(Incoming)
class IncomingAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    model=Incoming
    list_display = (
        'month', 'tracking_number', 'date_received',
        'received_by', 'received_from', 'received_from_1', 'document_type',
        'particulars', 'endorsed_to', 'date_endorsed', 'date_acted_upon', 'actions_taken',
    )

    list_filter = (
        ('group', DropdownFilter),
        ('received_by', RelatedDropdownFilter),
        ('document_type', RelatedDropdownFilter),
    )

    search_fields = ['tracking_number', 'particulars', 'received_from']
    resource_class = IncomingResource

    def month(self, incoming):
        return incoming.group.strftime('%B')

    def received_by(self, incoming):
        return incoming.received_by.get_short_name()

    def document_type(self, incoming):
        return incoming.document_type.name

