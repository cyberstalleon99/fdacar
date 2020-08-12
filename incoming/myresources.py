from import_export import resources
from import_export.fields import Field

class IncomingResource(resources.ModelResource):
    group =             Field(column_name="Month")
    tracking_number =   Field(attribute="tracking_number", column_name="Tracking Number")
    date_received =     Field(attribute="date_received", column_name="Date Received")
    received_by =       Field(column_name="Received by")
    received_from =     Field(attribute="received_from", column_name="Received From")
    received_from_1 =   Field(attribute="received_from_1", column_name="Received From (Company/Establishment Name)")
    document_type =     Field(column_name="Type of Document")
    particulars =       Field(attribute="particulars", column_name="Particulars")
    endorsed_to =       Field(attribute="endorsed_to", column_name="Endorsed to")
    date_endorsed =     Field(attribute="date_endorsed", column_name="Date Endorsed")
    date_acted_upon =   Field(attribute="date_acted_upon", column_name="Date Acted Upon")
    actions_taken =     Field(attribute="actions_taken", column_name="Actions Taken")

    def dehydrate_group(self, incoming):
        return incoming.group.strftime('%B')

    def dehydrate_received_by(self, incoming):
        return incoming.received_by.get_short_name()

    def dehydrate_document_type(self, incoming):
        return incoming.document_type.name
