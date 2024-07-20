from django import forms

class DataForm(forms.Form):
    address = forms.CharField()
    latitude = forms.DecimalField()
    longitude = forms.DecimalField()
