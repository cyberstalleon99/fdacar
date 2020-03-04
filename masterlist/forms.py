from django import forms
from django.utils import timezone
from .models import Establishment, AdditionalActivity, AuthorizedOfficer, QualifiedPerson, \
    PrimaryActivity, PlantAddress, WarehouseAddress, OfficeAddress, \
    Province, CityOrMunicipality, ProductType, SpecificActivity, ProductLine, AuthorizedOfficerDesignation, QualifiedPersonDesignation

EST_STATUS = [
    ('A', 'Active'),
    ('I', 'Inactive')
]

class StepOneForm(forms.ModelForm):
    class Meta:
        model = Establishment
        fields = ['application', 'name', 'product_type', 'primary_activity', 'specific_activity',
                  'additional_activity', 'product_line', 'remarks']

        widgets = {
            'name': forms.Textarea(
                attrs={'rows': 2, 'cols': 40, 'placeholder': 'Enter Name of Establishment here...'}),
            'specific_activity':forms.CheckboxSelectMultiple,
            'remarks':forms.Textarea(
                attrs={'rows': 2, 'cols': 40, 'placeholder': 'Enter Name of Products here...'})
        }

    # issuance = forms.DateTimeField(widget=forms.SelectDateWidget())
    issuance = forms.DateTimeField()
    lto_number = forms.CharField(max_length=20)
    expiry = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_line'].queryset=ProductLine.objects.none()

        if 'product_type' in self.data:
            try:
                product_type_id = int(self.data.get('product_type'))
                self.fields['product_line'].queryset = ProductLine.objects.filter(product_type_id=product_type_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['product_line'].queryset = self.instance.fields['product_type'].product_line_set.order_by('name')


# Plant Address Form
class StepTwoAForm(forms.ModelForm):
    class Meta:
        model = PlantAddress
        fields = ('address', 'region', 'province', 'municipality_or_city')
        widgets = {
            'address':forms.Textarea(attrs={'rows': 2, 'cols': 40, 'placeholder': 'House No./Street Name/Barangay...'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].queryset = Province.objects.none()
        self.fields['municipality_or_city'].queryset = CityOrMunicipality.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['province'].queryset = Province.objects.filter(region_id=region_id).order_by('name')
                province_id = int(self.data.get('province'))
                self.fields['municipality_or_city'].queryset = CityOrMunicipality.objects.filter(province_id=province_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['province'].queryset = self.instance.region.province_set.order_by('name')

# Warehouse Address Form
class StepTwoBForm(StepTwoAForm):
    pass

# Office Address Form
class StepTwoCForm(StepTwoAForm):
    pass

class StepThreeForm(forms.Form):
    authorized_firstname = forms.CharField(max_length=20, label='First Name')
    authorized_lastname = forms.CharField(max_length=20, label='Last Name')
    authorized_middleinit = forms.CharField(max_length=1, label='Middle Initial')
    authorized_desig = forms.ModelChoiceField(queryset=AuthorizedOfficerDesignation.objects.all(), label='Designation')

    qualified_firstname = forms.CharField(max_length=20, label='First Name')
    qualified_lastname = forms.CharField(max_length=20, label='Last Name')
    qualified_middleinit = forms.CharField(max_length=1, label='Middle Initial')
    qualified_desig = forms.ModelChoiceField(queryset=QualifiedPersonDesignation.objects.all(), label='Designation')
    status = forms.ChoiceField(choices=EST_STATUS)



