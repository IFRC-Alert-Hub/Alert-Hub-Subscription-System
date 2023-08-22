import json
from django.core.cache import cache
from subscription_dir.models import Subscription
def cache_subscriptions_alert():
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        pass
        #cache_subscription_alert(subscription)
#def cache_subscription_alert(subscription):
    #subscription_alerts_list = cache.get("subscription" + str(subscription.id))
    #cache.set("subscription" + str(subscription.id), subscription_alerts_list, timeout=None)

def cache_incoming_alert_for_subscription(subscription, alert):
    subscription_alerts_dict = cache.get("subscription" + str(subscription.id))
    #print(subscription_alerts_list)
    if subscription_alerts_dict is None:
        subscription_alerts_dict = {}

    subscription_alerts_dict[alert.id] = json.loads(alert.serialised_string)
    cache.set("subscription" + str(subscription.id), subscription_alerts_dict, timeout=None)


def cache_deleted_alert_for_subscription(subscription, alert):
    subscription_alerts_dict = cache.get("subscription" + str(subscription.id))
    del subscription_alerts_dict[alert.id]
    cache.set("subscription" + str(subscription.id), subscription_alerts_dict, timeout=None)

def delete_subscription_alerts(subscription_id):
    return cache.delete("subscription" + str(subscription_id))

def get_subscription_alerts(subscription_id):
    subscription_alerts_dict = cache.get("subscription" + str(subscription_id))

    if subscription_alerts_dict is None:
        return False
    return subscription_alerts_dict


def cache_subscriptions_admins():
    for subscription in Subscription.objects.all():
        cache_subscription_admins(subscription)

def cache_subscription_admins(subscription):
    for admin1_id in subscription.admin1_ids:
        cache_id = "admin"+str(admin1_id)
        admin = cache.get(cache_id)
        if admin is None:
            cache.set(cache_id, [subscription.id])
        else:
            admin.append(subscription.id)
            cache.set(cache_id,admin)

def delete_subscription_admins_cache(subscription):
    for admin1_id in subscription.admin1_ids:
        cache_id = "admin"+str(admin1_id)
        admin = cache.get(cache_id)
        if admin is not None:
            try:
                admin.remove(subscription.id)
                cache.set(cache_id, admin)
            except ValueError:
                pass

def get_admin_cache(admin_id):
    return cache.get("admin"+str(admin_id))

def clear_cache():
    cache.clear()
