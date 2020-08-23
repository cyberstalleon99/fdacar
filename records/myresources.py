from import_export import resources
from import_export.fields import Field
from .models import Inspection

class InspectionResource(resources.ModelResource):
    tracking_number =           Field(attribute="tracking_number", column_name="DTN/Case No.")
    name =                      Field(column_name="Name")
    address =                   Field(column_name="Address")
    product_type =              Field(column_name="Product Type")
    primary_activity =          Field(column_name="Primary Activity")
    specific_activity =         Field(column_name="Specific Activity/s")
    lto =                       Field(column_name="LTO Number")
    lto_expiry =                Field(column_name="Expiry")
    inspection_type =           Field(column_name="Purpose of Inspection")
    date_inspected =            Field(column_name="Date Inspected")
    frequency_of_inspection =   Field(attribute="frequency_of_inspection", column_name="Frequency of Inspection")
    risk_rating =               Field(attribute="risk_rating", column_name="Risk Rating")
    inspector =                 Field(column_name="Inspected by")
    capa_date_received =        Field(column_name="Date Received CAPA")
    capa_count =                Field(column_name="No. of CAPA")
    date_forwarded =            Field(attribute="date_forwarded", column_name="Date Forwarded to Supervisor")
    date_approved =             Field(attribute="date_approved", column_name="Date Approved to Supervisor")
    remarks =                   Field(column_name="Remarks")

    def dehydrate_name(self, inspection):
        return inspection.record.establishment.name

    def dehydrate_address(self, inspection):
        return inspection.record.establishment.plant_address.full_address()

    def dehydrate_product_type(self, inspection):
        return inspection.record.establishment.product_type.name

    def dehydrate_primary_activity(self, inspection):
        return inspection.record.establishment.primary_activity.name

    def dehydrate_specific_activity(self, inspection):
        return inspection.record.establishment.specific_activities()

    def dehydrate_lto(self, inspection):
        try:
            inspection.record.establishment.ltos.first().lto_number
        except:
            return "N/A"
        else:
            return inspection.record.establishment.ltos.first().lto_number

    def dehydrate_lto_expiry(self, inspection):
        try:
            inspection.record.establishment.ltos.first().expiry
        except:
            return "N/A"
        else:
            return inspection.record.establishment.ltos.first().expiry

    def dehydrate_inspection_type(self, inspection):
        return inspection.inspection_type

    def dehydrate_date_inspected(self, inspection):
        return inspection.date_inspected

    def dehydrate_inspector(self, inspection):
        return ",\n".join(s.inspector.get_short_name()  for s in inspection.est_inspectors.all())

    def dehydrate_capa_date_received(self, inspection):
        try:
            inspection.capa.date_submitted
        except:
            return "N/A"
        else:
            return inspection.capa.date_submitted

    def dehydrate_capa_count(self, inspection):
        try:
            inspection.capa.date_submitted
        except:
            return "N/A"
        else:
            return inspection.capadeficiency__set.count()

    def dehydrate_remarks(self, inspection):
        return inspection.remarks


    class Meta:
        model = Inspection
        exclude = ('id', 'record', 'date_of_followup_inspection', 'for_capa', 'inspection_report', 'type_of_inspection', 'capa')


