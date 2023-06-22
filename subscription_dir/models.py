from django.db import models


class User:
    id = models.IntegerField(primary_key=True, default=0)
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")
    whatsapp_id = models.CharField(blank=True, null=True, max_length=255, verbose_name="whatsapp")


class Region:
    id = models.IntegerField(primary_key=True, default=0)
    name = models.CharField(default="None")
    polygon = models.CharField(default="None")


class Subscription(models.Model):
    userId = models.ForeignKey(User, related_name='userId', on_delete=models.CASCADE)
    regionId = models.ForeignKey(Region, related_name='regionId', on_delete=models.CASCADE)
    category = models.CharField(default="", verbose_name="category")
    urgency = models.CharField(default="", verbose_name="category")
    severity = models.CharField(default="", verbose_name="severity")
    subscribeBy = models.CharField(default="", verbose_name="subscribeBy")

