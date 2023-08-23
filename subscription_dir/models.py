import json

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    subscription_name = models.CharField(default="", verbose_name="subscription_name")
    user_id = models.IntegerField(default=0, verbose_name="user_id")
    country_ids = ArrayField(models.IntegerField(verbose_name='country_ids'), default=list)
    admin1_ids = ArrayField(models.IntegerField(verbose_name='admin1_ids'), default=list)
    urgency_array = ArrayField(models.CharField(verbose_name='urgency_array'), default=list)
    severity_array = ArrayField(models.CharField(verbose_name='severity_array'), default=list)
    certainty_array = ArrayField(models.CharField(verbose_name='certainty_array'), default=list)
    subscribe_by = ArrayField(models.CharField(verbose_name="subscribe_by"), default=list)
    sent_flag = models.IntegerField(default=0, verbose_name="sent_flag")

    def subscription_alerts_to_dict(self):
        alerts_list = []
        alerts = self.alert_set.all()

        for alert in alerts:
            alerts_list.append(json.loads(alert.serialised_string))
        return alerts_list

    def save(self, *args, force_insert=False, force_update=False, **kwargs):
        from subscription_manager_dir import subscription_alert_mapping, cache
        super().save(force_insert, force_update, *args, **kwargs)
        self.alert_set.clear()
        subscription_alert_mapping.map_subscription_to_alert(self)
        #cache.cache_subscription_alert(self)
        #cache.cache_subscription_admins(self)

    def delete(self, *args, force_insert=False, force_update=False):
        from subscription_manager_dir import cache
        cache_instance = cache.dynamic_cache()
        cache_instance.delete_subscription_alerts(self.id)
        #cache.delete_subscription_admins_cache(self)
        super().delete(force_insert, force_update)
