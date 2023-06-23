from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")
    whatsapp_id = models.CharField(blank=True, null=True, max_length=255, verbose_name="whatsapp")


class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(default="None")
    polygon = models.CharField(default="None")


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    region = models.ForeignKey(Region, related_name='region', on_delete=models.CASCADE)
    category = models.CharField(default="", verbose_name="category")
    urgency = models.IntegerField(default="", verbose_name="urgency")
    severity = models.IntegerField(default="", verbose_name="severity")
    subscribe_by = models.CharField(default="", verbose_name="subscribe_by")
