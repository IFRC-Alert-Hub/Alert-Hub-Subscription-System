from django import forms
from .models import alert

class AlertForm(forms.ModelForm):
    class Meta:
        model = alert
        fields = ['headline', 'category', 'event', 'urgency', 'severity', 'certainty']
