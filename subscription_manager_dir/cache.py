import json
from django.core.cache import cache
from subscription_dir.models import Subscription
def cache_subscriptions_alert():
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        cache_subscription_alert(subscription)
def cache_subscription_alert(subscription):
    subscription_alerts_dict = subscription.subscription_alerts_to_dict()
    cache.set("subscription" + str(subscription.id), json.dumps(
        subscription_alerts_dict, indent=None), timeout=None)


def get_subscription_alerts(subscription_id):
    return cache.get("subscription" + str(subscription_id))