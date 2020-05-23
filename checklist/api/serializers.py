from rest_framework import serializers
from masterlist.api.serializers import EstablishmentSerializer
from checklist.models import Job

class RenewalSerializer(serializers.ModelSerializer):
    establishment = EstablishmentSerializer(many=False)
    date_created = serializers.SerializerMethodField()

    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()

    def get_DT_RowId(self, job):
        return 'row_%d' % job.establishment.pk

    def get_DT_RowAttr(self, job):
        return {'pkey': job.establishment.pk}

    def get_date_created(self, job):
        return job.date_created.date()

    class Meta:
        model = Job
        fields = ('DT_RowId', 'DT_RowAttr', 'establishment', 'date_created', 'inspection_status')

        datatables_always_serialize = ('id',)
