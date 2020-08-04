from import_export import resources
from import_export.fields import Field
from .models import Pli

class PliResource(resources.ModelResource):
    status = Field(attribute="status", column_name="Status")
    name = Field(column_name="Name")
    address = Field(column_name="Address")
    month = Field(column_name="Month")
    product_type = Field(column_name="Product Type")
    primary_activity = Field(column_name="Primary Activity")
    specific_activity = Field(column_name="Specific Activity/s")
    lto = Field(column_name="LTO Number")
    lto_expiry = Field(column_name="Expiry")
    type_of_inspection = Field(column_name="Purpose of Inspection")
    date_inspected = Field(column_name="Date Inspected")
    inspector = Field(column_name="Inspected by")
    remarks = Field(column_name="Remarks")

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
        specific_activities = ''
        for spec_act in pli.inspection.record.establishment.specific_activity.all():
            specific_activities += spec_act.name + ", "
        return specific_activities

    def dehydrate_lto(self, pli):
        return pli.inspection.record.establishment.ltos.latest()

    def dehydrate_lto_expiry(self, pli):
        return pli.inspection.record.establishment.ltos.latest().expiry

    def dehydrate_type_of_inspection(self, pli):
        return pli.inspection.type_of_inspection

    def dehydrate_date_inspected(self, pli):
        return pli.inspection.date_inspected

    def dehydrate_inspector(self, pli):
        return pli.inspection.inspector.get_short_name()

    def dehydrate_remarks(self, pli):
        return pli.inspection.remarks


    class Meta:
        model = Pli
        exclude = ('id', 'group', 'inspection', 'mother_dtn', 'date_forwarded_to_center')
