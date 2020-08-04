from rest_framework import serializers
from pli.models import Pli
from records.api.serializers import InspectionSerializer

class PliSerializer(serializers.ModelSerializer):
    status      = serializers.StringRelatedField()
    inspection  = InspectionSerializer(many=False)
    group       = serializers.SerializerMethodField()
    DT_RowId    = serializers.SerializerMethodField()
    est_id      = serializers.SerializerMethodField()
    DT_RowAttr  = serializers.SerializerMethodField()

    def get_DT_RowId(self, pli):
        # return 'row_%d' % pli.pk
        return pli.inspection.record.establishment.pk

    def get_DT_RowAttr(self, pli):
        return {'pkey': pli.pk}

    def get_group(self, pli):
        return pli.group.strftime('%B')

    def get_est_id(self, pli):
        return pli.inspection.record.establishment.pk

    class Meta:
        model = Pli
        fields = (
            'DT_RowId', 'DT_RowAttr','id',
            'group', 'mother_dtn', 'date_forwarded_to_center', 'status', 'inspection', 'est_id'
        )