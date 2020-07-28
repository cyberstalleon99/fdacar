from rest_framework import serializers
from incoming.models import Incoming

class IncomingSerializer(serializers.ModelSerializer):
    received_by = serializers.StringRelatedField()
    document_type = serializers.StringRelatedField()
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()

    def get_DT_RowId(self, incoming):
        return 'row_%d' % incoming.pk

    def get_DT_RowAttr(self, incoming):
        return {'pkey': incoming.pk}

    class Meta:
        model = Incoming
        fields = (
            'DT_RowId', 'DT_RowAttr','id', 'dtn', 'date_received', 'received_by', 'received_from',
            'received_from_1', 'document_type', 'particulars', 'endorsed_to', 'date_endorsed', 'date_acted_upon', 'actions_taken',
        )
