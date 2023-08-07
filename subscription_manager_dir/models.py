# These files are used for storing required models of subscriptions and their correlated alerts
from django.db import models
from subscription_dir.models import Subscription
from django.contrib.postgres.fields import ArrayField
from subscription_manager_dir.external_alert_models import CapFeedAlert
class SubscriptionAlerts(models.Model):
    subscription = models.OneToOneField(Subscription, primary_key=True, on_delete=models.CASCADE)
    alert_ids = ArrayField(models.IntegerField(verbose_name='alert_ids'), default=list)

    def subscription_alerts_to_dict(self):
        alerts_list = []
        alert_ids = self.alert_ids

        for alert_id in alert_ids:
            alert = CapFeedAlert.objects.using("AlertDB").get(id=alert_id)
            alerts_list.append(alert.to_dict())
        return alerts_list
