from rest_framework import serializers
from outgoing.models import Outgoing

class OutgoingSerializer(serializers.ModelSerializer):
    document_type = serializers.StringRelatedField()
    courier = serializers.StringRelatedField()
    forwarded_by = serializers.StringRelatedField()
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()

    def get_DT_RowId(self, outgoing):
        return 'row_%d' % outgoing.pk

    def get_DT_RowAttr(self, outgoing):
        return {'pkey': outgoing.pk}

    class Meta:
        model = Outgoing
        fields = (
            'DT_RowId', 'DT_RowAttr','id', 'group', 'tracking_number', 'document_type', 'particulars', 'remarks', 'courier', 'courier_tracking_number',
            'forwarded_by', 'date_forwarded', 'forwarded_to', 'forwarded_to_1',
        )