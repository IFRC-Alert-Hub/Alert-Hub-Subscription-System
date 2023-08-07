# This models is used for getting all alerts in the Alert Database
from django.db import models

class CapFeedCountry(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'cap_feed_country'

class CapFeedAdmin1(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey('CapFeedCountry', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_admin1'


class CapFeedAlert(models.Model):
    id = models.BigAutoField(primary_key=True)
    sent = models.DateTimeField()
    country = models.ForeignKey('CapFeedCountry', models.DO_NOTHING)
    admin1s = models.ManyToManyField(CapFeedAdmin1, through='CapFeedAlertadmin1')

    class Meta:
        managed = False
        db_table = 'cap_feed_alert'

class CapFeedAlertadmin1(models.Model):
    id = models.BigAutoField(primary_key=True)
    admin1 = models.ForeignKey(CapFeedAdmin1, models.DO_NOTHING)
    alert = models.ForeignKey(CapFeedAlert, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_alertadmin1'


class CapFeedAlertinfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.CharField()
    event = models.CharField(max_length=255)
    urgency = models.CharField()
    severity = models.CharField()
    certainty = models.CharField()
    alert = models.ForeignKey(CapFeedAlert, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cap_feed_alertinfo'



