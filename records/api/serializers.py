from rest_framework import serializers
from records.models import Inspection, Record
from masterlist.api.serializers import EstablishmentSerializer

class RecordSerializer(serializers.ModelSerializer):
    establishment = EstablishmentSerializer(many=False)
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()

    def get_DT_RowId(self, record):
        return 'row_%d' % record.pk

    def get_DT_RowAttr(self, record):
        return {'pkey': record.pk}

    class Meta:
        model = Record
        fields = ('DT_RowId', 'DT_RowAttr','id', 'folder_id', 'establishment')


class InspectionSerializer(serializers.ModelSerializer):
    record = RecordSerializer(many=False)
    inspector = serializers.SerializerMethodField()
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()

    def get_DT_RowId(self, inspection):
        return 'row_%d' % inspection.pk

    def get_DT_RowAttr(self, inspection):
        return {'pkey': inspection.pk}

    def get_inspector(self, inspection):
        return ",\n".join(inspector.inspector.get_short_name()  for inspector in inspection.est_inspectors.all())

    class Meta:
        model = Inspection
        fields = (
            'DT_RowId', 'DT_RowAttr','id', 'tracking_number', 'type_of_inspection',
            'date_inspected', 'frequency_of_inspection', 'risk_rating', 'date_of_followup_inspection', 'record',
            'inspector', 'remarks', 'date_forwarded', 'date_approved'
        )
