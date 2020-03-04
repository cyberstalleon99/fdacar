from django.db import models
from django.utils import timezone

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
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    middle_initial = models.CharField(max_length=1, null=True, blank=True)

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

class AuthorizedOfficer(Person):
    designation = models.ForeignKey(AuthorizedOfficerDesignation, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name()

class Lto(models.Model):
    issuance = models.DateTimeField('date issued')
    lto_number = models.CharField(max_length=20)
    expiry = models.DateTimeField('expiry date')

    def __str__(self):
        return self.lto_number

class Region(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Province(models.Model):
    name = models.CharField(max_length=30)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class CityOrMunicipality(models.Model):
    name = models.CharField(max_length=30)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Address(models.Model):
    address = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    municipality_or_city = models.ForeignKey(CityOrMunicipality, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.address

    def full_address(self):
        return self.address + ', ' + self.municipality_or_city.name + ', ' + self.province.name

class PlantAddress(Address):
    pass

class WarehouseAddress(Address):
    pass

class OfficeAddress(Address):
    pass

class Establishment(models.Model):
    date_modified = models.DateTimeField('date modified', default=timezone.now)

    # Step One Form Fields
    APPLICATIONS = [
        ('I', 'Initial'),
        ('R', 'Renewal'),
        ('V', 'Variation')
    ]
    application = models.CharField(max_length=1, choices=APPLICATIONS)
    name = models.CharField(max_length=60)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
    center = models.CharField(max_length=6)
    primary_activity = models.ForeignKey(PrimaryActivity, on_delete=models.CASCADE, null=True)
    lto = models.OneToOneField(Lto, on_delete=models.CASCADE)
    specific_activity = models.ManyToManyField(SpecificActivity)
    additional_activity = models.ForeignKey(AdditionalActivity, on_delete=models.SET_NULL, null=True)
    product_line = models.ForeignKey(ProductLine, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    # Step Two A Form Fields
    plant_address = models.ForeignKey(PlantAddress, on_delete=models.CASCADE, null=True, blank=True)

    # Step Two B Form Fields
    warehouse_address = models.ForeignKey(WarehouseAddress, on_delete=models.CASCADE, null=True, blank=True)

    # Step Two C Form Fields
    office_address = models.ForeignKey(OfficeAddress, on_delete=models.CASCADE, null=True, blank=True)

    # Added radiologist as a Designation for Qualified Person; not as a separate model
    # radiologist = models.ForeignKey(Radiologist, on_delete=models.CASCADE, null=True, blank=True)
    authorized_officer = models.ForeignKey(AuthorizedOfficer, on_delete=models.CASCADE, null=True, blank=True)
    # qualified_person = models.ForeignKey(QualifiedPerson, on_delete=models.CASCADE, null=True, blank=True)
    # inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, null=True, blank=True)
    EST_STATUS = [
        ('I', 'Inactive'),
        ('A', 'Active')
    ]
    status = models.CharField(max_length=1, choices=EST_STATUS, null=True, blank=True)

    def __str__(self):
        return self.name

class QualifiedPerson(Person):
    establishment = models.ForeignKey(Establishment, on_delete=models.SET_NULL, null=True)
    designation = models.ForeignKey(QualifiedPersonDesignation, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name()

class Inspection(models.Model):
    establishment = models.ForeignKey(Establishment, on_delete=models.SET_NULL, null=True)
    INSPECTION_TYPES = [
        ('PLI', 'Post Licensing Inspection'),
        ('REN', 'Renewal of LTO'),
        ('INI', 'Initial Inspection'),
        ('RTN', 'Routine Inspection')
    ]
    type_of_inspection = models.CharField(max_length=20, choices=INSPECTION_TYPES)
    date_inspected = models.DateTimeField('date_inspected')
    frequency_of_inspection = models.IntegerField(default=0)
    RISK_RATINGS = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]
    risk_rating = models.CharField(max_lengt=7, choices=RISK_RATINGS)
    date_of_followup_inspection = models.DateTimeField('date_followup_inspection')
    INSPECTORS = [
        ('GGM', 'Giovanni G. Monang'),
        ('RTB', 'Rochelle T. Bayanes'),
        ('NDN', 'Nadia D. Navarro'),
        ('SOP', 'Saturnina O. Pandosen')
    ]
    inspector = models.CharField(max_length=3, choices=INSPECTORS)
    remarks = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.date_inspected

class CapaPreparator(Person):
    # designation =
    pass

class Capa(models.Model):
    start_date = models.DateTimeField('start_date')
    prepared_by = models.ForeignKey(CapaPreparator, on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.CharField(max_length=10, choices=Inspection.INSPECTORS)
    date_submitted = models.DateTimeField('date_submitted')
    date_approved = models.DateTimeField('date_approved')
    remks = models.CharField(max_length=200)

class CapaDeficiency(models.Model):
    capa = models.ForeignKey(Capa, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=200)
    action = models.CharField(max_length=200)
    evidence = models.FileField()
    CAPA_TYPES = [
        ('Critical', 'Critical'),
        ('Major', 'Major'),
        ('Others', 'Others')
    ]
    type = models.CharField(max_length=10, choices=CAPA_TYPES)
    proposed_comletion_date = models.DateTimeField()
    inspector_comment = models.CharField(max_length=200)
    accepted = models.BooleanField(default=False)









