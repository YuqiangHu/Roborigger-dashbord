from django import forms

class MakepdfForm(forms.Form):
    title = forms.CharField(max_length=32)
    csvfile = forms.CharField(max_length=32)