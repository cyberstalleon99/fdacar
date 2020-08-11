from import_export import resources
from import_export.fields import Field
from .models import Application
from dateutil.relativedelta import relativedelta

class ApplicationResource(resources.ModelResource):
    status = Field(attribute="status", column_name="Status")
    tracking_number = Field(attribute="tracking_number", column_name="Tracking Number")
    group = Field(attribute="group", column_name="Month")
    establishment = Field(column_name="Name")
    plant_address = Field(column_name="Address")
    province = Field(column_name="Province")
    city_or_municipality = Field(column_name="City or Municipality")
    product_type = Field(column_name="Product Type")
    primary_activity = Field(column_name="Primary Activity")
    specific_activity = Field(column_name="Specific Activity")
    lto = Field(column_name="LTO Number")
    lto_expiry = Field(column_name="Expiry")
    application_type = Field(attribute="application_type", column_name="Application Type")
    type_of_variation = Field(attribute="type_of_variation", column_name="Varition Type")
    payment = Field(attribute="payment", column_name="Payment")
    date_received_by_rfo = Field(attribute="date_received_by_rfo", column_name="Date Posted")
    date_received_by_inspector = Field(attribute="date_received_by_inspector", column_name="Date Received by Inspector")
    inspector = Field(column_name="Inspector")
    date_inspected = Field(column_name="Date Inspected")
    notes_on_inspection = Field(column_name="Notes on inspection")
    date_accomplished = Field(attribute="date_accomplished", column_name="Date Accomplished")
    capa_start_date = Field(column_name="CAPA Start Date")
    capa_date_received = Field(column_name="CAPA Date Received")
    capa_processing_duration = Field(column_name="Processing Duration (CAPA)")
    recommendation = Field(attribute="recommendation", column_name="Recommendation")
    date_approved_by_supervisor = Field(attribute="date_approved_by_supervisor", column_name="Date Approved by Supervisor")
    processing_duration = Field(attribute="processing_duration", column_name="Processing Duration (Eportal)")
    eod_1 = Field(attribute="eod_1", column_name="EOD no Inspection")
    eod_2 = Field(attribute="eod_2", column_name="EOD w/ Inspection")
    backlog = Field(attribute="backlog", column_name="Backlog")
    reason_1 = Field(attribute="reason_1", column_name="Reason for Backlog")

    def dehydrate_establishment(self, app):
        return app.establishment.name

    def dehydrate_group(self, app):
        return app.group.strftime('%B')

    def dehydrate_plant_address(self, app):
        return app.establishment.plant_address.address

    def dehydrate_province(self, app):
        return app.establishment.plant_address.province.name

    def dehydrate_city_or_municipality(self, app):
        return app.establishment.plant_address.municipality_or_city.name

    def dehydrate_product_type(self, app):
        return app.establishment.product_type.name

    def dehydrate_primary_activity(self, app):
        return app.establishment.primary_activity.name

    def dehydrate_specific_activity(self, app):
        specific_activities = ''
        for spec_act in app.establishment.specific_activity.all():
            specific_activities += spec_act.name + ", "
        return specific_activities

    def dehydrate_lto(self, app):
        return app.establishment.ltos.latest()

    def dehydrate_lto_expiry(self, app):
        return app.establishment.ltos.latest().expiry

    def dehydrate_inspector(self, app):
        return app.inspection.inspector

    def dehydrate_date_inspected(self, app):
        return app.inspection.date_inspected

    def dehydrate_notes_on_inspection(self, app):
        return app.inspection.remarks

    def dehydrate_capa_start_date(self, app):
        try:
            app.inspection.capa.date_prepared
        except:
            return None
        else:
            return app.inspection.capa.date_prepared

    def dehydrate_capa_date_received(self, app):
        try:
            app.inspection.capa.date_submitted
        except:
            return None
        else:
            return app.inspection.capa.date_submitted

    def dehydrate_capa_processing_duration(self, app):
        try:
            app.inspection.capa.date_prepared
            app.inspection.capa.date_submitted
        except:
            return None
        else:
            start_date = app.inspection.capa.date_prepared
            end_date = app.inspection.capa.date_submitted
            difference = relativedelta(end_date, start_date)
            return difference

    class Meta:
        model = Application
        exclude = (
                    'id', 'applied_thru', 'date_forwarded_to_inspector',
                    'inspection', 'licensing_officer', 'date_received_by_supervisor', 'date_forwarded_to_center_1',
                    'date_returned_by_center', 'reason_2', 'date_forwarded_to_center_2',
        )


