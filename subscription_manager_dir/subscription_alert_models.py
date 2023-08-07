# These files are used for storing required models of subscriptions and their correlated alerts
from django.db import models
from subscription_dir.models import Subscription
from django.contrib.postgres.fields import ArrayField

class SubscriptionAlerts(models.Model):

    subscription = models.OneToOneField(Subscription, primary_key=True, on_delete=models.CASCADE)
    alert_ids = ArrayField(models.IntegerField(verbose_name='alert_ids'), default=list)


    def subscription_alerts_to_dict(self):
        alerts_dict = []
        #alerts = self.alert_ids.all()
        #for alert in alerts:
        #    alerts_dict.append(alert.to_dict())
        return alerts_dict
