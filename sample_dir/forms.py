from django import forms
from .models import alert

class AlertForm(forms.ModelForm):
    class Meta:
        model = alert
        fields = ['name', 'desc', 'integer', 'creation_date']
