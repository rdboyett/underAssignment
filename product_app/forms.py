import re

from django import forms
from django.core.validators import RegexValidator

from models import PurchaseHistory



class PurchaseHistoryForm(forms.Form):
    name = forms.CharField(label='Full Name', max_length=65, min_length=3, widget=forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'minlength':3}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'required':'true'}))
    price = forms.FloatField(widget=forms.HiddenInput, initial=0.0)
    phone = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class': 'form-control', 'phoneUS':'true', 'required':'true'}), validators=[RegexValidator(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$', 'Enter a valid phone number.')])
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'required':'true'}))

    def cleanPhone(self):
        phonePattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')
        cleanPhone = str(self.cleaned_data['phone'])
        phoneData = phonePattern.search(cleanPhone).groups()
        return '(%s) %s-%s' % (phoneData[0], phoneData[1], phoneData[2])
    
    
