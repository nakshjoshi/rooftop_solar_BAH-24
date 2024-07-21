from django import forms

class DataForm(forms.Form):
    address = forms.CharField(required=False)
    latitude = forms.DecimalField(required=False, decimal_places=8, max_digits=10)
    longitude = forms.DecimalField(required=False, decimal_places=8, max_digits=10)
