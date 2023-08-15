import json

from .cache import cache_subscription_alert
from .external_alert_models import CapFeedAlert, CapFeedAdmin1
from .models import Alert, Subscription
from .tasks import process_immediate_alerts


def map_subscriptions_to_alert():
    for subscription in Subscription.objects.all():
        map_subscription_to_alert(subscription)


def map_subscription_to_alert(subscription):
    for admin1_id in subscription.admin1_ids:
        admin1 = CapFeedAdmin1.objects.filter(id=admin1_id).first()
        if admin1 is None:
            continue
        potential_alert_set = admin1.capfeedalert_set.all()

        for alert in potential_alert_set:
            for info in alert.capfeedalertinfo_set.all():
                if info.severity in subscription.severity_array and \
                        info.certainty in subscription.certainty_array and \
                        info.urgency in subscription.urgency_array:
                    internal_alert = Alert.objects.filter(id=alert.id).first()
                    if internal_alert is None:
                        internal_alert = Alert.objects.create(id=alert.id,
                                                              serialised_string=json.dumps(
                                                                  alert.to_dict()))
                        internal_alert.save()
                    internal_alert.subscriptions.add(subscription)
                    break


def map_alert_to_subscription(alert_id):
    alert = CapFeedAlert.objects.filter(id=alert_id).first()
    converted_alert = Alert.objects.filter(id=alert_id).first()
    if alert is None:
        return f"Alert with id {alert_id} is not existed"
    if converted_alert is not None:
        return f"Alert with id {alert_id} is already converted and matched subscription"
    alert_admin1_ids = []
    for admin1 in alert.admin1s.all():
        alert_admin1_ids.append(admin1.id)
    subscriptions = Subscription.objects.filter(admin1_ids__overlap=alert_admin1_ids)

    internal_alert = None
    updated_subscription_ids = []
    for subscription in subscriptions:
        for info in alert.capfeedalertinfo_set.all():
            if info.severity in subscription.severity_array and \
                    info.certainty in subscription.certainty_array and \
                    info.urgency in subscription.urgency_array:
                if internal_alert is None:
                    internal_alert = Alert.objects.create(id=alert.id, serialised_string=json.dumps(
                        alert.to_dict()))
                    internal_alert.save()
                internal_alert.subscriptions.add(subscription)
                # Update the cache when related alerts are added
                cache_subscription_alert(subscription)
                updated_subscription_ids.append(subscription.id)
                break

        if subscription.sent_flag == 0:
            process_immediate_alerts(subscription.id)

    if len(updated_subscription_ids) != 0:
        return f"Incoming Alert {alert_id} is successfully converted. Mapped Subscription id are " \
               f"{updated_subscription_ids}."

    return f"Incoming Alert {alert_id} is not mapped with any subscription."


def delete_alert_to_subscription(alert_id):
    alert_to_be_deleted = Alert.objects.filter(id=alert_id).first()
    if alert_to_be_deleted is None:
        return f"Alert with id {alert_id} has not been found in subscription database."

    subscriptions = alert_to_be_deleted.subscriptions.all()
    updated_subscription_ids = []
    for subscription in subscriptions:
        subscription.alert_set.remove(alert_to_be_deleted)
        # Update the cache when related alerts are removed
        cache_subscription_alert(subscription)
        updated_subscription_ids.append(subscription.id)

    alert_to_be_deleted.delete()
    if len(updated_subscription_ids) != 0:
        return f" Alert {alert_id} is successfully deleted from subscription database. " \
               f"Updated Subscription id are " \
               f"{updated_subscription_ids}."

    return f"Alert {alert_id} is successfully deleted from subscription database. "


def print_all_admin1s_in_country(country_id):
    ids = []
    admin1s = CapFeedAdmin1.objects.filter(country__id=country_id)
    for admin in admin1s:
        ids.append(admin.id)

def get_subscription_alerts_without_cache(subscription_id):
    subscription = Subscription.objects.filter(id=subscription_id).first()
    if subscription is None:
        return False
    else:
        map_subscription_to_alert(subscription)
        subscription_alerts_dict = subscription.subscription_alerts_to_dict()
        return json.dumps(subscription_alerts_dict, indent=None)