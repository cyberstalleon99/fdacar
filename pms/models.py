from django.db import models
from masterlist.models import Establishment
from accounts.models import User

class Classification(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ReferralType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class DosageForm(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class CollectionMode(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class AnalysisRequest(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Unit(models.Model):
    unit = models.CharField(max_length=250)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.unit

class Product(models.Model):
    date_collected =        models.DateField(verbose_name="Date Collected")
    tracking_number =       models.CharField(max_length=12, verbose_name="DTN/Case No.")
    date_request_received = models.DateField(verbose_name="Date of Request Letter Received", null=True, blank=True)
    date_of_referral =      models.DateField(verbose_name="Date of Referral")
    classification =        models.ForeignKey(Classification, on_delete=models.DO_NOTHING, verbose_name="PMS Classification")
    type_of_referral =      models.ForeignKey(ReferralType, on_delete=models.DO_NOTHING, verbose_name="Type of Referral")
    establishment =         models.ForeignKey(Establishment, on_delete=models.DO_NOTHING, verbose_name="Establishment")
    product_category =      models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING, verbose_name="Product Category")
    dosage_form =           models.ForeignKey(DosageForm, on_delete=models.DO_NOTHING, verbose_name="Dosage Form")
    generic_name =          models.CharField(max_length=250, verbose_name="Generic Name")
    brand_name =            models.CharField(max_length=250, verbose_name="Brand Name")
    cpr_number =            models.CharField(max_length=250, verbose_name="CPR No.")
    batch_lot_number =      models.CharField(max_length=250, verbose_name="Batch/Lot No.")
    date_manufactured =     models.DateField(verbose_name="Manufacuring Date")
    date_exiry =            models.DateField(verbose_name="Expiration Date")
    tmr_name =              models.CharField(max_length=250, verbose_name="Trader/Mfg/Repacker's Name")
    tmr_address =           models.TextField(verbose_name="Trader/Mfg/Repacker's Address")
    distributor_name =      models.CharField(max_length=250, verbose_name="Distributor's Name")
    distributor_address =   models.TextField(verbose_name="Distributor's Address")
    collection_mode =       models.ForeignKey(CollectionMode, on_delete=models.DO_NOTHING, verbose_name="Mode of Collection")
    inspector =             models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Inspector")
    remarks =               models.DateField(verbose_name="Remarks")
    quantity =              models.PositiveIntegerField(verbose_name="Number of Samples")
    unit =                  models.ForeignKey(Unit, on_delete=models.DO_NOTHING)
    unit_cost =             models.DecimalField(max_digits=10, decimal_places=2)
    or_number =             models.CharField(max_length=250, verbose_name="OR Number")
    total_cost =            models.DecimalField(max_digits=10, decimal_places=2)
    date_forwarded =        models.DateField()
    date_result_received =  models.DateField()
    result =                models.TextField()
    analysis_request =      models.ForeignKey(AnalysisRequest, on_delete=models.DO_NOTHING, verbose_name="Analysis Request (For Lab Analysis only)")
    csl_reference_number =  models.CharField(max_length=250, verbose_name="CSL Control Ref. No.")
    center_remarks =        models.TextField(verbose_name="Remarks of Centers")
    action =                models.CharField(max_length=250, verbose_name="Action Take by RFO")
    warning_letter =        models.CharField(max_length=250, null=True, blank=True)
