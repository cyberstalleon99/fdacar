from import_export import resources
from import_export.fields import Field
from .models import Establishment, SpecificActivity, Lto, ProductType
from checklist.models import Job

class EstablishmentResource(resources.ModelResource):
    name = Field(attribute="name", column_name="Establishment Name")
    product_type = Field(attribute="product_type__name", column_name="Product Type")
    primary_activity = Field(attribute="primary_activity__name", column_name="Primary Activity")
    specific_activity = Field(column_name="Specific Activity/s")
    product_line = Field(attribute="product_line__name", column_name="Product Line")
    remarks = Field(attribute="remarks", column_name="Product Remarks")
    lto = Field(column_name="LTO Number")
    lto_expiry = Field(column_name="Expiry")
    plant_address = Field(attribute="plant_address__address", column_name="Address")
    province = Field(attribute="plant_address__province__name", column_name="Province")
    municipality_or_city = Field(attribute="plant_address__municipality_or_city__name", column_name="City or Municipality")
    contact_number = Field(attribute="authorized_officer__mobile", column_name="Contact Number")
    email = Field(attribute="authorized_officer__email", column_name="Email Address")
    status = Field(attribute="status", column_name="Status")
    folder_id = Field(attribute="folder_id", column_name="Folder Number")

    def dehydrate_specific_activity(self, establishment):
        specific_activities = ''
        for spec_act in establishment.specific_activity.all():
            specific_activities += spec_act.name + ", "
        return specific_activities

    def dehydrate_lto(self, establishment):
        return establishment.ltos.latest()

    def dehydrate_lto_expiry(self, establishment):
        return establishment.ltos.latest().expiry.date()

    class Meta:
        model=Establishment
        exclude = ('id', 'date_modified', 'application', 'center', 'additional_activity', 'office_address', 'authorized_officer',)

class JobResource(resources.ModelResource):
    name = Field(attribute="establishment__name", column_name="Establishment Name")
    product_type = Field(attribute="establishment__product_type__name", column_name="Product Type")
    primary_activity = Field(attribute="establishment__primary_activity__name", column_name="Primary Activity")
    specific_activity = Field(column_name="Specific Activity/s")
    product_line = Field(attribute="establishment__product_line__name", column_name="Product Line")
    remarks = Field(attribute="establishment__remarks", column_name="Product Remarks")
    lto = Field(column_name="LTO Number")
    lto_expiry = Field(column_name="Expiry")
    plant_address = Field(attribute="establishment__plant_address__address", column_name="Address")
    province = Field(attribute="establishment__plant_address__province__name", column_name="Province")
    municipality_or_city = Field(attribute="establishment__plant_address__municipality_or_city__name", column_name="City or Municipality")
    contact_number = Field(attribute="establishment__authorized_officer__mobile", column_name="Contact Number")
    email = Field(attribute="establishment__authorized_officer__email", column_name="Email Address")
    status = Field(attribute="establishment__status", column_name="Status")
    folder_id = Field(attribute="establishment__folder_id", column_name="Folder Number")

    def dehydrate_specific_activity(self, job):
        specific_activities = ''
        for spec_act in job.establishment.specific_activity.all():
            specific_activities += spec_act.name + ", "
        return specific_activities

    def dehydrate_lto(self, job):
        return job.establishment.ltos.latest()

    def dehydrate_lto_expiry(self, job):
        return job.establishment.ltos.latest().expiry.date()

    class Meta:
        model=Job
        exclude = ('id', 'date_modified', 'application', 'center', 'additional_activity', 'office_address', 'authorized_officer',)
