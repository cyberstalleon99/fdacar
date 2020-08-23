from import_export import resources
from import_export.fields import Field
from .models import Pli

class PliResource(resources.ModelResource):
    status =                    Field(attribute="status", column_name="Status")
    tracking_number =           Field(column_name="DTN/Case No.")
    name =                      Field(column_name="Name")
    address =                   Field(column_name="Address")
    month =                     Field(column_name="Month")
    product_type =              Field(column_name="Product Type")
    primary_activity =          Field(column_name="Primary Activity")
    specific_activity =         Field(column_name="Specific Activity/s")
    lto =                       Field(column_name="LTO Number")
    lto_expiry =                Field(column_name="Expiry")
    inspection_type =           Field(column_name="Purpose of Inspection")
    date_inspected =            Field(column_name="Date Inspected")
    frequency_of_inspection =   Field(column_name="Frequency of Inspection")
    risk_rating =               Field(column_name="Risk Rating")
    inspector =                 Field(column_name="Inspected by")
    capa_date_received =        Field(column_name="Date Received CAPA")
    capa_count =                Field(column_name="No. of CAPA")
    remarks =                   Field(column_name="Remarks")

    def dehydrate_tracking_number(self, pli):
        return pli.inspection.tracking_number

    def dehydrate_name(self, pli):
        return pli.inspection.record.establishment.name

    def dehydrate_address(self, pli):
        return pli.inspection.record.establishment.plant_address.full_address()

    def dehydrate_month(self, pli):
        return pli.group.strftime('%B')

    def dehydrate_product_type(self, pli):
        return pli.inspection.record.establishment.product_type.name

    def dehydrate_primary_activity(self, pli):
        return pli.inspection.record.establishment.primary_activity.name

    def dehydrate_specific_activity(self, pli):
        return pli.inspection.record.establishment.specific_activities()

    def dehydrate_lto(self, pli):
        try:
            pli.inspection.record.establishment.ltos.first().lto_number
        except:
            return "N/A"
        else:
            return pli.inspection.record.establishment.ltos.first().lto_number

    def dehydrate_lto_expiry(self, pli):
        try:
            pli.inspection.record.establishment.ltos.first().expiry
        except:
            return "N/A"
        else:
            return pli.inspection.record.establishment.ltos.first().expiry

    def dehydrate_inspection_type(self, pli):
        return pli.inspection.inspection_type

    def dehydrate_date_inspected(self, pli):
        return pli.inspection.date_inspected

    def dehydrate_frequency_of_inspection(self, pli):
        return pli.inspection.frequency_of_inspection

    def dehydrate_risk_rating(self, pli):
        return pli.inspection.risk_rating

    def dehydrate_inspector(self, pli):
        return ",\n".join(s.inspector.get_short_name()  for s in pli.inspection.est_inspectors.all())

    def dehydrate_capa_date_received(self, pli):
        try:
            pli.inspection.capa.date_submitted
        except:
            return "N/A"
        else:
            return pli.inspection.capa.date_submitted

    def dehydrate_capa_count(self, pli):
        try:
            pli.inspection.capa.date_submitted
        except:
            return "N/A"
        else:
            return pli.inspection.capadeficiency__set.count()

    def dehydrate_remarks(self, pli):
        return pli.inspection.remarks


    class Meta:
        model = Pli
        exclude = ('id', 'group', 'inspection', 'mother_dtn', 'date_forwarded_to_center')
