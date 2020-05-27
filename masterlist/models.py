from django.db import models
from django.utils import timezone
from . import constants
from datetime import datetime
from dateutil import relativedelta
from . import mymanagers
from django.conf import settings

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
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    middle_initial = models.CharField(max_length=3)
    email = models.EmailField(max_length=250, blank=True, null=True)
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
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    municipality_or_city = models.ForeignKey(CityOrMunicipality, on_delete=models.CASCADE)

    def __str__(self):
        return self.address

    def full_address(self):
        return self.address + ', ' + self.municipality_or_city.name + ', ' + self.province.name

class PlantAddress(Address):
    pass

class OfficeAddress(Address):
    pass

class AuthorizedOfficer(Person):
    designation = models.ForeignKey(AuthorizedOfficerDesignation, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name()

class Establishment(models.Model):
    date_modified = models.DateTimeField('date modified', default=timezone.now)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=60)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    center = models.CharField(max_length=6, choices=constants.CENTERS, default="CDRR")
    primary_activity = models.ForeignKey(PrimaryActivity, on_delete=models.CASCADE)
    specific_activity = models.ManyToManyField(SpecificActivity)
    plant_address = models.OneToOneField(PlantAddress, on_delete=models.SET_NULL, null=True)
    office_address = models.OneToOneField(OfficeAddress, on_delete=models.SET_NULL, null=True)
    authorized_officer = models.OneToOneField(AuthorizedOfficer, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=8, choices=constants.EST_STATUS, null=True, default="Active")
    expiredlist = mymanagers.ExpiredListManager()
    inactivelist = mymanagers.InactiveListManager()
    objects = models.Manager()

    @property
    def test(self):
        pass

    def __str__(self):
        return self.name + " - " + self.plant_address.address + "(" + self.specific_activities() + ")"

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
    issuance = models.DateField(null=True, blank=True, verbose_name='Date Issued', help_text='Format: YYYY/MM/DD')
    lto_number = models.CharField(max_length=255)
    expiry = models.DateField('expiry date', help_text='Format: YYYY/MM/DD')

    def __str__(self):
        return self.lto_number

    def get_duration(self):
        start_date = datetime.now().date()
        end_date = self.expiry
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
    designation = models.ForeignKey(QualifiedPersonDesignation, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name()
