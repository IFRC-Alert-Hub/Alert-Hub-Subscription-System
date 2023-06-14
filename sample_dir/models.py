from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now
# Create your models here.
class alert(models.Model):
    category = models.CharField(default="no category")
    event = models.CharField( default="hazard")
    urgency = models.CharField(default="low")
    severity = models.CharField( default="low")
    certainty = models.CharField( default="low")
    effective = models.CharField( default = now())
    senderName = models.CharField(max_length=100, default= "Null")
    headline = models.CharField(max_length=100, default= "Empty Headline")
    description = models.CharField(max_length=255,default= "Empty Description")
    instruction = models.CharField(max_length=255,default= "Empty Instruction")
    areaDesc = models.CharField(max_length=255, default= "None")
    polygon = ArrayField(models.FloatField())
    geocode_name = models.CharField(default= "None")
    geocode_value = models.CharField(default= "None")
    processed_time = models.TimeField(auto_now=True)
