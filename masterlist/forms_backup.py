from django import forms
from django.utils import timezone
from .models import Establishment, AdditionalActivity, AuthorizedOfficer, QualifiedPerson, \
    PrimaryActivity, PlantAddress, WarehouseAddress, OfficeAddress, \
    Province, CityOrMunicipality, ProductType, SpecificActivity, ProductLine

EST_STATUS = [
    ('I', 'Inactive'),
    ('A', 'Active')
]

class StepOneForm(forms.Form):
    application = forms.ChoiceField(choices=Establishment.APPLICATIONS)
    name = forms.CharField(max_length=100, label='Name of Establishment', widget=forms.Textarea(attrs=
                                                                                                {'rows': 2,
                                                                                                 'cols': 40,
                                                                                                 'placeholder': 'Enter Name of Establishment here...'}
                                                                                                ))
    product_type = forms.ModelChoiceField(queryset=ProductType.objects.all())
    primary_activity = forms.ModelChoiceField(queryset=PrimaryActivity.objects.all())
    specific_activity = forms.ModelMultipleChoiceField(queryset=SpecificActivity.objects.all(), widget=forms.CheckboxSelectMultiple)
    additional_activity = forms.ModelChoiceField(queryset=AdditionalActivity.objects.all())
    product_line = forms.ModelChoiceField(queryset=ProductLine.objects.all())
    remarks = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter products here..'}))
    # issuance = forms.DateTimeField(widget=forms.SelectDateWidget())
    issuance = forms.DateTimeField()
    lto_number = forms.CharField(max_length=20)
    expiry = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_line'].queryset=ProductLine.objects.none()

        # if 'product_type' in self.data:
        #     try:
        #         product_type_id = int(self.data.get('product_type'))
        #         self.fields['product_line'].queryset = ProductLine.objects.filter(product_type_id=product_type_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass
        # elif self.pk:
        #     self.fields['product_line'].queryset = self.fields['product_type'].product_line_set.order_by('name')


# Plant Address Form
class StepThreeAForm(forms.ModelForm):
    class Meta:
        model = PlantAddress
        fields = ('address', 'region', 'province', 'municipality_or_city')

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
class StepThreeBForm(forms.ModelForm):
    class Meta:
        model = WarehouseAddress
        fields = ('address', 'region', 'province', 'municipality_or_city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].queryset = Province.objects.none()
        self.fields['municipality_or_city'].queryset = CityOrMunicipality.objects.none()

# Office Address Form
class StepThreeCForm(forms.ModelForm):
    class Meta:
        model = OfficeAddress
        fields = ('address', 'region', 'province', 'municipality_or_city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].queryset = Province.objects.none()
        self.fields['municipality_or_city'].queryset = CityOrMunicipality.objects.none()

class StepFourForm(forms.Form):
    authorized_firstname = forms.CharField(max_length=20, label='First Name')
    authorized_lastname = forms.CharField(max_length=20, label='Last Name')
    authorized_middleinit = forms.CharField(max_length=1, label='Middle Initial')
    authorized_desig = forms.ChoiceField(choices=AuthorizedOfficer.DESIGNATIONS, label='Designation')

    qualified_firstname = forms.CharField(max_length=20, label='First Name')
    qualified_lastname = forms.CharField(max_length=20, label='Last Name')
    qualified_middleinit = forms.CharField(max_length=1, label='Middle Initial')
    qualified_desig = forms.ChoiceField(choices=QualifiedPerson.DESIGNATIONS, label='Designation')
    status = forms.ChoiceField(choices=EST_STATUS)



