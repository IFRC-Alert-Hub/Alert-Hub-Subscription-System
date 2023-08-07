import json
from django.core.cache import cache

def cache_subscription_alert(subscription_alerts):
    subscription_alerts_dict = subscription_alerts.subscription_alerts_to_dict()
    print("id is:" + str(subscription_alerts.id))
    cache.set("subscription" + str(subscription_alerts.subscription.id), json.dumps(
        subscription_alerts_dict,
        indent=None), timeout=None)


def get_subscription_alerts(subscription_id):
    return cache.get("subscription" + str(subscription_id))