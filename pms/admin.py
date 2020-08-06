from django.contrib import admin
from .models import Product, Classification, ReferralType, ProductCategory, DosageForm, CollectionMode, AnalysisRequest, Unit, ProductEstablishment, ProductAddress, ProductSpecificActivity

admin.site.register(Classification)
admin.site.register(ReferralType)
admin.site.register(ProductCategory)
admin.site.register(DosageForm)
admin.site.register(CollectionMode)
admin.site.register(AnalysisRequest)
admin.site.register(Product)
admin.site.register(Unit)
admin.site.register(ProductEstablishment)
admin.site.register(ProductAddress)
admin.site.register(ProductSpecificActivity)
