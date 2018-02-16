from django.forms import ModelForm
from django import forms
from client.models import System

class SystemForm(ModelForm):
    class Meta:
        model = System
        fields = '__all__'
        widgets = {
            'contract_date': forms.DateInput(attrs={'class':'datepicker'}),
            'install_date': forms.DateInput(attrs={'class':'datepicker'}),
        }
