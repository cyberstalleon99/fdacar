from django.db import models
from django.utils import timezone
from . import constants
from datetime import datetime
from dateutil import relativedelta
from . import mymanagers
from . import constants

class ProductType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class PrimaryActivity(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class AdditionalActivity(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class SpecificActivity(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class ProductLine(models.Model):
    name = models.CharField(max_length=150)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Person(models.Model):
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    middle_initial = models.CharField(max_length=3, null=True, blank=True)
    email = models.EmailField(max_length=250, null=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return self.first_name + " " + self.middle_initial + ". " + self.last_name

class QualifiedPersonDesignation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class AuthorizedOfficerDesignation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50, null=True)

    def __str__(self):
        str = ''
        if self.description:
            str = self.name + ' (' + self.description + ' )'
        else:
            str = self.name
        return str

class Province(models.Model):
    name = models.CharField(max_length=30)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class CityOrMunicipality(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        str = ''
        if self.description:
            str = self.name + ' (' + self.description + ' )'
        else:
            str = self.name
        return str

class Address(models.Model):
    address = models.CharField(max_length=250)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    municipality_or_city = models.ForeignKey(CityOrMunicipality, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.address

    def full_address(self):
        return self.address + ', ' + self.municipality_or_city.name + ', ' + self.province.name

class PlantAddress(Address):
    pass

class OfficeAddress(Address):
    pass

class AuthorizedOfficer(Person):
    designation = models.ForeignKey(AuthorizedOfficerDesignation, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name()

class Establishment(models.Model):
    date_modified = models.DateTimeField('date modified', default=timezone.now)
    name = models.CharField(max_length=60)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
    center = models.CharField(max_length=6, choices=constants.CENTERS)
    primary_activity = models.ForeignKey(PrimaryActivity, on_delete=models.CASCADE, null=True)
    specific_activity = models.ManyToManyField(SpecificActivity)
    # additional_activity = models.ForeignKey(AdditionalActivity, on_delete=models.SET_NULL, null=True)
    # product_line = models.ForeignKey(ProductLine, on_delete=models.SET_NULL, null=True, blank=True)
    plant_address = models.OneToOneField(PlantAddress, on_delete=models.SET_NULL, null=True)
    office_address = models.OneToOneField(OfficeAddress, on_delete=models.SET_NULL, null=True)
    authorized_officer = models.OneToOneField(AuthorizedOfficer, on_delete=models.SET_NULL, null=True)
    # remarks = models.CharField(max_length=100, null=True, blank=True, verbose_name='Product Remarks')
    status = models.CharField(max_length=8, choices=constants.EST_STATUS, null=True, default="Active")
    expiredlist = mymanagers.ExpiredListManager()
    objects = models.Manager()

    def __str__(self):
        return self.name + " - " + self.plant_address.address

    def specific_activities(self):
        return ",\n".join(s.name for s in self.specific_activity.all())

    class Meta:
        ordering = ['-date_modified']

class EstAdditionalActivity(models.Model):
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='additional_activities')
    additional_activity = models.ForeignKey(AdditionalActivity, on_delete=models.CASCADE)

    def __str__(self):
        return self.additional_activity.name

class EstProductLine(models.Model):
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='product_lines')
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=100, null=True, blank=True, verbose_name='Product Remarks')

    def __str__(self):
        return self.product_line.name

class WarehouseAddress(Address):
    establishment = models.ForeignKey(Establishment, on_delete=models.SET_NULL, null=True, related_name='warehouses')
    pass

class VariationType(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=constants.VARIATION_TYPES)
    # primary_activity = models.ForeignKey(PrimaryActivity, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " - " + self.type

class Lto(models.Model):
    type_of_application = models.CharField(max_length=20, choices=constants.APPLICATIONS)
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, null=True, related_name='ltos')
    issuance = models.DateTimeField(null=True, blank=True, verbose_name='Date Issued')
    lto_number = models.CharField(max_length=20)
    expiry = models.DateTimeField('expiry date')
    # Variation = models.ForeignKey(Variation, on_delete=models.CASCADE)

    # type_of_variation = models.ForeignKey(VariationType, on_delete=models.CASCADE, null=True)
    # old = models.CharField(max_length=255, verbose_name="From", help_text="Enter old value here (if applicable)")
    # current = models.CharField(max_length=255, verbose_name="To", help_text="Enter the new value here (if applicable)")
    # remarks = models.CharField(max_length=255)

    def __str__(self):
        return self.lto_number

    def get_duration(self):
        start_date = datetime.now().date()
        end_date = self.expiry.date()
        difference = relativedelta.relativedelta(end_date, start_date)
        month = difference.years * 12 + difference.months
        return month

    class Meta:
        ordering = ['-expiry']
        get_latest_by = 'expiry'

class Variation(models.Model):
    lto = models.ForeignKey(Lto, on_delete=models.CASCADE, related_name='variations')
    type_of_variation = models.ForeignKey(VariationType, on_delete=models.CASCADE, null=True)
    old = models.CharField(max_length=255, verbose_name="From", help_text="Applicable only to variations whose old values will be replaced with new values. Put N/A if not applicable")
    current = models.CharField(max_length=255, verbose_name="To", help_text="Applicable only to variations whose old values will be replaced with new values. Put N/A if not applicable.")
    remarks = models.CharField(max_length=255)

    def __str__(self):
        if self.type_of_variation:
            return self.type_of_variation.name
        else:
            return self.lto.lto_number
    def test(self):
        return self.objects.first()

class QualifiedPerson(Person):
    establishment = models.ForeignKey(Establishment, on_delete=models.SET_NULL, null=True)
    designation = models.ForeignKey(QualifiedPersonDesignation, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name()

# class Capa(models.Model):
#     start_date = models.DateTimeField('start_date')
#     approved_by = models.CharField(max_length=10, choices=constants.INSPECTORS)
#     date_submitted = models.DateTimeField('date_submitted')
#     date_approved = models.DateTimeField('date_approved')
#     remarks = models.CharField(max_length=200)
#
#     def __str__(self):
#         dateStr = self.start_date.strftime("%d %b %Y ")
#         return dateStr
#
# class CapaPreparator(Person):
#     capa = models.OneToOneField(Capa, on_delete=models.CASCADE, null=True)
#
#     class Meta:
#         verbose_name = 'Preparedy by'
#         verbose_name_plural = 'Prepared by'
#
# class CapaDeficiency(models.Model):
#     capa = models.ForeignKey(Capa, on_delete=models.SET_NULL, null=True, blank=True)
#     description = models.CharField(max_length=200)
#     action = models.CharField(max_length=200)
#     evidence = models.FileField(blank=True)
#
#     type = models.CharField(max_length=10, choices=constants.CAPA_TYPES)
#     proposed_comletion_date = models.DateTimeField(verbose_name="Proposed Completion Date")
#     inspector_comment = models.CharField(max_length=200, blank=True)
#     accepted = models.BooleanField(default=False)
#
#     def __str__(self):
#         return str(self.pk)
#
#     class Meta:
#         verbose_name = 'CAPA Deficiencies'
#         verbose_name_plural = 'CAPA Deficiencies'
#
# def report_directory_path(instance, filename):
#     return 'masterlist/inspection/ir_{0}/{1}'.format(instance.establishment.id, filename)
#
# class Inspection(models.Model):
#     establishment = models.ForeignKey(Establishment, on_delete=models.SET_NULL, null=True)
#     tracking_number = models.CharField(max_length=14, null=True, verbose_name="DTN or Case #")
#     capa = models.OneToOneField(Capa, on_delete=models.SET_NULL, null=True, blank=True)
#     type_of_inspection = models.CharField(max_length=20, choices=constants.INSPECTION_TYPES)
#     date_inspected = models.DateTimeField('Date Inspected')
#     frequency_of_inspection = models.PositiveIntegerField(default=0, verbose_name="Frequency of Inspection", null=True, blank=True)
#     risk_rating = models.CharField(max_length=7, choices=constants.RISK_RATINGS, null=True, blank=True)
#     date_of_followup_inspection = models.DateTimeField('Date of Followup Inspection', null=True, blank=True)
#     inspector = models.CharField(max_length=3, choices=constants.INSPECTORS)
#     remarks = models.CharField(max_length=200, null=True)
#     inspection_report = models.FileField(null=True, blank=False, upload_to=report_directory_path, verbose_name='Inspection Report')
#
#     def __str__(self):
#         dateStr = self.date_inspected.strftime("%d %b %Y ")
#         return dateStr
#
#     def get_followup_duration(self):
#         month = 0
#         if self.date_of_followup_inspection:
#             start_date = datetime.now().date()
#             end_date = self.date_of_followup_inspection.date()
#             difference = relativedelta.relativedelta(end_date, start_date)
#             month = difference.years * 12 + difference.months
#         return month
#
#     class Meta:
#         ordering = ['-date_inspected']
#         get_latest_by = 'date_inspected'
#
# def capa_attachments_directory_path(instance, filename):
#     return 'masterlist/inspection/attachments/report_{0}/{1}'.format(instance.capa.id, filename)
