from django import forms
from .models import User_Address
import re

class AddressForm(forms.ModelForm):
    class Meta:
        model = User_Address
        fields = ['fullname','contact_number','house_name', 'landmark','city',  'pincode', 'district', 'state','country']
    
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs )
        self.fields['fullname'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['fullname'].widget.attrs['data-type'] = 'form-text'

        self.fields['contact_number'].widget.attrs['placeholder'] = 'Mobile'
        self.fields['contact_number'].widget.attrs['data-type'] = 'form-number'

        self.fields['house_name'].widget.attrs['placeholder'] = 'House Name'
        self.fields['house_name'].widget.attrs['data-type'] = 'form-text'

        self.fields['landmark'].widget.attrs['placeholder'] = 'Landmark'
        self.fields['landmark'].widget.attrs['data-type'] = 'form-text'

        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['city'].widget.attrs['data-type'] = 'form-text'

        self.fields['pincode'].widget.attrs['placeholder'] = 'Pincode'
        self.fields['pincode'].widget.attrs['data-type'] = 'form-number'

        self.fields['district'].widget.attrs['placeholder'] = 'District'
        self.fields['district'].widget.attrs['data-type'] = 'form-text'

        self.fields['state'].widget.attrs['placeholder'] = 'State'
        self.fields['state'].widget.attrs['data-type'] = 'form-text'

        self.fields['country'].widget.attrs['placeholder'] = 'Country'
        self.fields['country'].widget.attrs['data-type'] = 'form-text'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-md w-100'


    def clean_fullname(self):
        fullname = self.cleaned_data['fullname']
        if not re.match(r'^[a-zA-Z ]+$', fullname):
            raise forms.ValidationError("Name can only contain alphabets and spaces.")
        return fullname
    
    def clean_contact_number(self):
        contact_number = self.cleaned_data['contact_number']
        if str(contact_number).startswith('0'):
            raise forms.ValidationError('Phone number should not start with zero')
        if len(str(contact_number)) < 10:
            raise forms.ValidationError('Phone number should have minimum 10 numbers without start with zero')
        if len(str(contact_number)) > 12:
            raise forms.ValidationError('Phone number never greater than 12')
        return contact_number