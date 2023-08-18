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

def delete_subscription_alerts(subscription_id):
    return cache.delete("subscription" + str(subscription_id))

def get_subscription_alerts(subscription_id):
    result = cache.get("subscription" + str(subscription_id))
    if result is None:
        return False
    return result
def cache_subscriptions_admins():
    for subscription in Subscription.objects.all():
        cache_subscription_admins(subscription)

def cache_subscription_admins(subscription):
    for admin1_id in subscription.admin1_ids:
        cache_id = "admin"+str(admin1_id)
        admin = cache.get(cache_id)
        if admin == None:
            cache.set(cache_id, {subscription.id})
        else:
            admin.add(subscription.id)
            cache.set(cache_id,admin)

def delete_subscription_admins_cache(subscription):
    for admin1_id in subscription.admin1_ids:
        cache_id = "admin"+str(admin1_id)
        admin = cache.get(cache_id)
        if admin != None:
            try:
                admin.remove(subscription.id)
                cache.set(cache_id, admin)
            except ValueError:
                pass

def get_admin_cache(subscription_id):
    return cache.get("admin"+str(subscription_id))

def clear_cache():
    cache.clear()