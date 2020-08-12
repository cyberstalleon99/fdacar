from import_export import resources
from import_export.fields import Field

class ProductResource(resources.ModelResource):
    status = Field(attribute="status", column_name="Status")
    generic_name = Field(attribute="generic_name", column_name="Generic Name")
    brand_name = Field(attribute="brand_name", column_name="Brand Name")
    month = Field(column_name="Month")
    date_collected = Field(attribute="date_collected", column_name="Date Collected")
    tracking_number = Field(attribute="tracking_number", column_name="Tracking Number")
    classification = Field(column_name="Classification")
    type_of_referral = Field(column_name="Type of Referral")
    analysis_request = Field(column_name="Analysis Request")
    establishment = Field(column_name="Establishment")
    product_category = Field(column_name="Product Category")
    collection_mode = Field(column_name="Collection Mode")
    inspector = Field(column_name="Inspector/s")
    date_forwarded = Field(attribute="date_forwarded", column_name="Date Forwarded")
    date_result_received = Field(attribute="date_result_received", column_name="Date Result Received")
    result = Field(attribute="result", column_name="Result")
    center_remarks = Field(attribute="center_remarks", column_name="Remarks of Center")

    def dehydrate_month(self, product):
        return product.group.strftime('%B')

    def dehydrate_classification(self, product):
        return product.classification.name

    def dehydrate_type_of_referral(self, product):
        return product.type_of_referral.name

    def dehydrate_analysis_request(self, product):
        return product.analysis_request.name

    def dehydrate_establishment(self, product):
        return product.establishment.name

    def dehydrate_address(self, product):
        return product.establishment.address.full_address()

    def dehydrate_product_category(self, product):
        return product.product_category.name

    def dehydrate_collection_mode(self, product):
        return product.collection_mode.name

    def dehydrate_inspector(self, product):
        return ",\n".join(s.product_inspector.get_short_name()  for s in product.product_inspectors.all())


