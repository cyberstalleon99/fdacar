from import_export import resources
from import_export.fields import Field

class OutgoinResource(resources.ModelResource):
    group =                     Field(column_name="Month")
    tracking_number =           Field(attribute="tracking_number", column_name="Tracking Number")
    document_type =             Field(column_name="Type of Document")
    particulars =               Field(attribute="particulars", column_name="Particulars")
    remarks =                   Field(attribute="remarks", column_name="Remarks")
    courier =                   Field(column_name="Courier")
    courier_tracking_number =   Field(attribute="courier_tracking_number", column_name="Courier Tracking Number")
    date_forwarded =            Field(attribute="date_forwarded", column_name="Date Forwarded")
    forwarded_by =              Field(column_name="Forwarded by")
    forwarded_to =              Field(attribute="forwarded_to", column_name="Forwarded to")
    forwarded_to_1 =            Field(attribute="forwarded_to_1", column_name="Forwarded to  (Company/Establishment Name)")

    def dehydrate_group(self, outgoing):
        return outgoing.group.strftime('%B')

    def dehydrate_document_type(self, outgoing):
        return outgoing.document_type.name

    def dehydrate_courier(self, outgoing):
        return outgoing.courier.name

    def dehydrate_forwarded_by(self, outgoing):
        return outgoing.forwarded_by.get_short_name()