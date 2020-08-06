from rest_framework import serializers
from masterlist.models import Establishment, Lto, ProductType
from dateutil.relativedelta import relativedelta

class LtoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lto
        fields = (
            'id', 'lto_number', 'expiry'
        )

        datatables_always_serialize = ('id',)

class ProductTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductType
        fields = (
            'id', 'name'
        )

        datatables_always_serialize = ('id',)

class EstablishmentSerializer(serializers.ModelSerializer):
    product_type = ProductTypeSerializer()
    ltos = LtoSerializer(read_only=True, many=True)
    specific_activities = serializers.SerializerMethodField()
    plant_address = serializers.SerializerMethodField()
    primary_activity = serializers.StringRelatedField()
    duration = serializers.SerializerMethodField()
    folder_number = serializers.SerializerMethodField()
    last_inspection = serializers.SerializerMethodField()
    next_inspection = serializers.SerializerMethodField()
    # extra = serializers.SerializerMethodField()

    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()

    # def get_extra(self, establishment):
    #     return establishment.ltos.latest().type_of_application + " - " + establishment.record.inspections.count()

    def get_next_inspection(self, establishment):
        next_date_inspection = ''

        try:
            establishment.record.inspections.latest()
        except:
            return 'No inspections yet'
        else:
            frequency_of_inspection = establishment.record.inspections.latest().frequency_of_inspection
            if frequency_of_inspection:
                next_date_inspection = establishment.record.inspections.latest().date_inspected + relativedelta(years=int(frequency_of_inspection))
            else:
                return 'No Risk Assessment'
        return next_date_inspection

    def get_DT_RowId(self, establishment):
        return 'row_%d' % establishment.pk

    def get_DT_RowAttr(self, establishment):
        return {'pkey': establishment.pk}

    def get_duration(self, establishment):
        return establishment.ltos.latest().get_duration()

    def get_last_inspection(self, establishment):
        try:
            establishment.record.inspections.latest().date_inspected
        except:
            return 'No inspections yet'
        else:
            return establishment.record.inspections.latest().date_inspected
            # return 'There are inspections'


    def get_folder_number(self, establishment):
        try:
            establishment.record
        except:
            return 'No file'
        else:
            return establishment.record.folder_id

    def get_specific_activities(self, establishment):
        return ', '.join([str(specific_activity) for specific_activity in establishment.specific_activity.all()])

    def get_plant_address(self, establishment):
        return establishment.plant_address.address + ', ' + establishment.plant_address.municipality_or_city.name + ', ' + establishment.plant_address.province.name


    class Meta:
        model = Establishment
        fields = (
            'DT_RowId', 'DT_RowAttr','id', 'specific_activities', 'name', 'center', 'status', 'product_type',
            'primary_activity', 'plant_address', 'authorized_officer',
            'ltos', 'duration', 'folder_number', 'last_inspection', 'next_inspection',
        )
