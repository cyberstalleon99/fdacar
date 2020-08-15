from rest_framework import serializers
from appsreceived.models import Application
from masterlist.api.serializers import EstablishmentSerializer
from records.api.serializers import InspectionSerializer
from dateutil.relativedelta import relativedelta

class AppsReceivedSerializer(serializers.ModelSerializer):
    group =                     serializers.SerializerMethodField()
    establishment =             EstablishmentSerializer()
    type_of_variation =         serializers.SerializerMethodField()
    # inspection =                InspectionSerializer()
    inspector =                 serializers.SerializerMethodField()
    date_inspected =            serializers.SerializerMethodField()
    inspection_remarks =        serializers.SerializerMethodField()
    capa_start_date =           serializers.SerializerMethodField()
    capa_date_received =        serializers.SerializerMethodField()
    capa_processing_duration =  serializers.SerializerMethodField()

    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()

    def get_DT_RowId(self, app):
        # return 'row_%d' % pli.pk
        return app.establishment.pk

    def get_DT_RowAttr(self, app):
        return {'pkey': app.pk}

    def get_group(self, app):
        return app.group.strftime('%B')

    def get_type_of_variation(self, app):
        try:
            app.type_of_variation.name
        except:
            return None
        else:
            return app.type_of_variation.name

    def get_capa_start_date(self, app):
        try:
            app.inspection.date_inspected
        except:
            return None
        else:
            return app.inspection.date_inspected

    def get_capa_date_received(self, app):
        try:
            app.inspection.capa.date_submitted
        except:
            return None
        else:
            return app.inspection.capa.date_submitted

    def get_capa_processing_duration(self, app):
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

    def get_inspector(self, app):
        try:
            app.inspection.est_inspectors.all()
        except:
            return "N/A"
        else:
            return ",\n".join(inspector.inspector.get_short_name()  for inspector in app.inspection.est_inspectors.all())

    def get_date_inspected(self, app):
        try:
            app.inspection.date_inspected
        except:
            return "N/A"
        else:
            return app.inspection.date_inspected

    def get_inspection_remarks(self, app):
        try:
            app.inspection.remarks
        except:
            return "N/A"
        else:
            return app.inspection.remarks

    class Meta:
        model = Application
        fields = (
            'DT_RowId', 'DT_RowAttr','id', 'status', 'tracking_number', 'group', 'establishment', 'application_type',
            'type_of_variation', 'payment', 'date_received_by_rfo', 'date_received_by_inspector', 'inspector', 'date_inspected',
            'inspection_remarks', 'date_accomplished', 'capa_start_date', 'capa_date_received',
            'capa_processing_duration', 'recommendation', 'date_approved_by_supervisor', 'processing_duration',
            'eod_1', 'eod_2', 'backlog', 'reason_1',
        )