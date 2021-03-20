from django import forms
from django.utils import timezone
from .models import Establishment, Address

EST_STATUS = [
    ('', '----------'),
    ('Inactive', 'Inactive (For unlicensed establishments)'),
    ('Closed', 'Closed (For closed establishments)'),
    ('Active', 'Active')
]

LTO_STATUS = [
    ('', '----------'),
    ('Valid', 'Valid'),
    ('Expired', 'Expired')
]

class MasterlistFilterForm(forms.ModelForm):
    status = forms.ChoiceField(choices=EST_STATUS)

    class Meta:
        model = Establishment
        fields = ['product_type', 'primary_activity', 'specific_activity', 'status',]

    def __init__(self, *args, **kwargs):
        super(MasterlistFilterForm, self).__init__(*args, **kwargs)
        self.fields['product_type'].required = False
        self.fields['primary_activity'].required = False
        self.fields['specific_activity'].required = False
        self.fields['status'].required = False

class ExpiredlistFilterForm(forms.ModelForm):

    class Meta:
        model = Establishment
        fields = ['product_type', 'primary_activity', 'specific_activity',]

    def __init__(self, *args, **kwargs):
        super(ExpiredlistFilterForm, self).__init__(*args, **kwargs)
        self.fields['product_type'].required = False
        self.fields['primary_activity'].required = False
        self.fields['specific_activity'].required = False

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['region', 'province', 'municipality_or_city']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['region'].required = False
        self.fields['province'].required = False
        self.fields['municipality_or_city'].required = False

