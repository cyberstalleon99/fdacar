from rest_framework import serializers
from pms.models import Product, ProductEstablishment

class EstablishmentSerializer(serializers.ModelSerializer):
    address                 = serializers.SerializerMethodField()
    primary_activity        = serializers.StringRelatedField()
    specific_activities     = serializers.SerializerMethodField()

    def get_address(self, establishment):
        return establishment.address.full_address()

    def get_specific_activities(self, establishment):
        return ', '.join([str(specific_activity) for specific_activity in establishment.specific_activity.all()])

    class Meta:
        model = ProductEstablishment
        fields = (
            'name', 'lto_number', 'expiry', 'primary_activity', 'specific_activities', 'address'
        )

class ProductSerializer(serializers.ModelSerializer):
    group               = serializers.SerializerMethodField()
    establishment       = EstablishmentSerializer(many=False)
    product_category    = serializers.StringRelatedField()
    collection_mode     = serializers.StringRelatedField()
    classification      = serializers.StringRelatedField()
    inspector           = serializers.SerializerMethodField()
    analysis_request    = serializers.StringRelatedField()
    type_of_referral    = serializers.StringRelatedField()
    DT_RowId            = serializers.SerializerMethodField()
    DT_RowAttr          = serializers.SerializerMethodField()

    def get_DT_RowId(self, product):
        # return 'row_%d' % product.pk
        return product.establishment.pk

    def get_DT_RowAttr(self, product):
        return {'pkey': product.pk}

    def get_group(self, product):
        return product.group.strftime('%B')

    def get_inspector(self, product):
        return product.inspector.get_short_name()

    class Meta:
        model = Product
        fields = (
            'DT_RowId', 'DT_RowAttr','id', 'group', 'generic_name', 'brand_name', 'date_collected',
            'tracking_number', 'classification', 'type_of_referral', 'analysis_request', 'establishment', 'product_category',
            'collection_mode', 'inspector', 'date_forwarded', 'date_result_received', 'result', 'center_remarks'
        )