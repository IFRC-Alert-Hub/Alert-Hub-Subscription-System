import json
from django.core.cache import cache

def cache_subscription_alert(subscription):
    subscription_alerts_dict = subscription.subscription_alerts_to_dict()
    print("id is:" + str(subscription.id))
    cache.set("subscription" + str(subscription.subscription.id), json.dumps(
        subscription_alerts_dict, indent=None), timeout=None)


def get_subscription_alerts(subscription_id):
    return cache.get("subscription" + str(subscription_id))