from django.db import models

from django.contrib.postgres.fields import ArrayField

from django.utils.timezone import now


class Alert(models.Model):
    hash_id = models.CharField()
    processed_time = models.DateTimeField(auto_now=True)


class AlertInfo(models.Model):
    alert = models.ForeignKey(Alert, related_name='infos', on_delete=models.CASCADE)

    category = models.CharField(default="no category")
    event = models.CharField(default="hazard")
    urgency = models.CharField(default="low")
    severity = models.CharField(default="low")
    certainty = models.CharField(default="low")
    effective = models.CharField(default=now())
    headline = models.CharField(max_length=100, default="Empty Headline")
    description = models.CharField(max_length=255, default="Empty Description")
    instruction = models.CharField(max_length=255, default="Empty Instruction")
    senderName = models.CharField(max_length=100, default="Null")

    areaDesc = models.CharField(max_length=255, default="None")
    polygon = models.CharField(max_length=255, default="None")
    geocode_name = models.CharField(default="None")
    geocode_value = models.CharField(default="None")

class Region(models.Model):
    id = models.IntegerField(primary_key=True, default=0)
    name = models.CharField(default="None")
    polygon = models.CharField(default="None")

class Country(models.Model):
    region_id =  models.ForeignKey(Region, related_name='region_id', on_delete=models.CASCADE, null=True)
    id = models.IntegerField(primary_key=True,default=0)
    name = models.CharField(default="None")
    society_name = models.CharField(default="None")
    polygon = models.CharField(default="None")
    centroid = models.CharField(default="None")