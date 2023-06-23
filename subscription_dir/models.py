from django.db import models
from django.contrib.postgres.fields import ArrayField


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0, verbose_name="user_id")
    country_ids = ArrayField(models.IntegerField(verbose_name='country_ids'), default=list)
    category = models.CharField(default="", verbose_name="category")
    urgency = models.IntegerField(default=0, verbose_name="urgency")
    severity = models.IntegerField(default=0, verbose_name="severity")
    subscribe_by = models.CharField(default="", verbose_name="subscribe_by")
