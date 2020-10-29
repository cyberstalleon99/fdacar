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
    # establishment       = EstablishmentSerializer(many=False)
    establishment_name  = serializers.SerializerMethodField()
    establishment_address  = serializers.SerializerMethodField()
    product_category    = serializers.StringRelatedField()
    collection_mode     = serializers.StringRelatedField()
    classification      = serializers.StringRelatedField()
    inspector           = serializers.SerializerMethodField()
    analysis_request    = serializers.StringRelatedField()
    type_of_referral    = serializers.StringRelatedField()

    # product_category    = serializers.SerializerMethodField()
    # collection_mode     = serializers.SerializerMethodField()
    # classification      = serializers.SerializerMethodField()
    # analysis_request    = serializers.SerializerMethodField()
    # type_of_referral    = serializers.SerializerMethodField()

    DT_RowId            = serializers.SerializerMethodField()
    DT_RowAttr          = serializers.SerializerMethodField()

    def get_DT_RowId(self, product):
        return 'row_%d' % product.pk
        # return product.establishment.pk

    def get_DT_RowAttr(self, product):
        return {'pkey': product.pk}

    def get_group(self, product):
        return product.group.strftime('%B')

    def get_establishment_name(self, product):
        try:
            product.establishment.name
        except:
            return product.remarks
        else:
            return product.establishment.name

    def get_establishment_address(self, product):
        try:
            product.establishment.name
        except:
            return product.remarks
        else:
            return product.establishment.address.full_address()

    # def get_product_category(self, product):
    #     return product.product_category.name

    # def get_collection_mode(self, product):
    #     return product.collection_mode.name

    # def get_classification(self, product):
    #     return product.classification.name

    # def get_analysis_request(self, product):
    #     return product.analysis_request.name

    # def get_type_of_referral(self, product):
    #     return product.type_of_referral.name

    def get_inspector(self, product):
        return ",\n".join(s.product_inspector.get_short_name()  for s in product.product_inspectors.all())

    class Meta:
        model = Product
        fields = (
            'DT_RowId', 'DT_RowAttr','id', 'status', 'group', 'generic_name', 'brand_name', 'date_collected',
            'tracking_number', 'classification', 'type_of_referral', 'analysis_request', 'establishment_name', 'establishment_address', 'product_category',
            'collection_mode', 'inspector', 'date_forwarded', 'date_result_received', 'result', 'center_remarks', 'remarks',
        )