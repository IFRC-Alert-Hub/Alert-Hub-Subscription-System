from django import forms
from .models import Alert, AlertInfo

class AlertForm(forms.ModelForm):
    class Meta:
        model = AlertInfo
        fields = ['headline', 'category', 'event', 'urgency', 'severity', 'certainty']
