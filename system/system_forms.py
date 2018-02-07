from django.forms import ModelForm
from client.models import System

class SystemForm(ModelForm):
    class Meta:
        model = System
        fields = '__all__'
