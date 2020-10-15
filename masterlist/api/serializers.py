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
    product_type =              ProductTypeSerializer()
    # ltos = LtoSerializer(read_only=True, many=True)
    lto_number =                serializers.SerializerMethodField()
    expiry =                    serializers.SerializerMethodField()
    specific_activities =       serializers.SerializerMethodField()
    plant_address =             serializers.SerializerMethodField()
    primary_activity =          serializers.StringRelatedField()
    duration =                  serializers.SerializerMethodField()
    last_inspection =           serializers.SerializerMethodField()
    next_inspection =           serializers.SerializerMethodField()
    inspection_type =           serializers.SerializerMethodField()

    owner =                     serializers.SerializerMethodField()
    contact_info =              serializers.SerializerMethodField()
    folder_number =             serializers.SerializerMethodField()
    application_type =          serializers.SerializerMethodField()

    DT_RowId =                  serializers.SerializerMethodField()
    DT_RowAttr =                serializers.SerializerMethodField()

    def get_next_inspection(self, establishment):
        next_date_inspection = ''

        try:
            establishment.record.inspections.latest()
        except:
            return 'For inspection'
        else:
            frequency_of_inspection = establishment.record.inspections.latest().frequency_of_inspection
            if frequency_of_inspection:
                next_date_inspection = establishment.record.inspections.latest().date_inspected + relativedelta(years=int(frequency_of_inspection))
            else:
                return 'No Risk Assessment'
        return next_date_inspection

    def get_inspection_type(self, establishment):

        try:
            establishment.record.inspections.latest().inspection_type.name
        except:
            return 'For inspection'
        else:
            return establishment.record.inspections.latest().inspection_type.name

    def get_DT_RowId(self, establishment):
        return 'row_%d' % establishment.pk

    def get_DT_RowAttr(self, establishment):
        return {'pkey': establishment.pk}

    def get_duration(self, establishment):
        try:
            establishment.ltos.latest().get_duration()
        except:
            return None
        else:
            return establishment.ltos.latest().get_duration()

    def get_last_inspection(self, establishment):
        try:
            establishment.record.inspections.latest().date_inspected
        except:
            return 'For inspection'
        else:
            return establishment.record.inspections.latest().date_inspected

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

    def get_application_type(self, establishment):
        try:
            establishment.ltos.latest().lto_number
        except:
            return "N/A"
        else:
            return establishment.ltos.latest().type_of_application
    
    def get_lto_number(self, establishment):
        try:
            establishment.ltos.latest().lto_number
        except:
            return "N/A"
        else:
            return establishment.ltos.latest().lto_number

    def get_expiry(self, establishment):
        try:
            establishment.ltos.latest().expiry
        except:
            return "N/A"
        else:
            return establishment.ltos.latest().expiry

    def get_owner(self, establishment):
        owner = establishment.authorized_officer.full_name()
        designation = establishment.authorized_officer.designation.name
        return owner + " (" + designation +")"

    def get_contact_info(self, establishment):
        mobile = ''
        email = ''

        if establishment.authorized_officer.mobile:
            mobile = establishment.authorized_officer.mobile
        else:
            mobile = "No mobile number"

        if establishment.authorized_officer.email:
            email = establishment.authorized_officer.email
        else:
            email = "No email address"

        return mobile + ", " + email

    class Meta:
        model = Establishment
        fields = (
            'DT_RowId', 'DT_RowAttr','id', 'specific_activities', 'name', 'center', 'status', 'product_type',
            'primary_activity', 'plant_address', 'authorized_officer', 'lto_number', 'expiry',
            'duration', 'folder_number', 'last_inspection', 'next_inspection', 'inspection_type', 'contact_info',
            'application_type', 'owner'
        )
