# These files are used for storing required models of subscriptions and their correlated alerts
from django.db import models
from subscription_dir.models import Subscription
from django.contrib.postgres.fields import ArrayField
from subscription_manager_dir.external_alert_models import CapFeedAlert

class Alert(models.Model):
    id = models.IntegerField(primary_key=True)
    subscriptions = models.ManyToManyField(Subscription,through="SubscriptionAlerts")
    serialised_string = models.CharField(max_length=255)

class SubscriptionAlerts(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)


