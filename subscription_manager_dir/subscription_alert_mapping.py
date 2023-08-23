import json

from django.db import transaction

from .cache import dynamic_cache
from .external_alert_models import CapFeedAlert, CapFeedAdmin1
from .models import Alert, Subscription
from .tasks import process_immediate_alerts


def map_subscriptions_to_alert():
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        map_subscription_to_alert(subscription)


def map_subscription_to_alert(subscription):
    cache_instance = dynamic_cache()
    cache_instance.delete_subscription_alerts(subscription.id)
    for admin1_id in subscription.admin1_ids:
        admin1 = CapFeedAdmin1.objects.filter(id=admin1_id).first()
        if admin1 is None:
            continue
        potential_alert_set = admin1.capfeedalert_set.all()

        for alert in potential_alert_set:
            #print(f"admin: {admin1_id} alert: {alert.id}")
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
                    cache_instance.cache_incoming_alert_for_subscription(subscription,
                                                                         internal_alert)
                    break
    cache_instance.update_cache()


def map_alert_to_subscription(alert_id):
    cache_instance = dynamic_cache()
    alert = CapFeedAlert.objects.filter(id=alert_id). \
        prefetch_related('admin1s', 'capfeedalertinfo_set').first()
    converted_alert = Alert.objects.filter(id=alert_id).first()

    if alert is None:
        return f"Alert with id {alert_id} is not existed"

    if converted_alert is not None:
        return f"Alert with id {alert_id} is already converted and matched subscription"

    alert_admin1_ids = [admin1.id for admin1 in alert.admin1s.all()]
    subscriptions = Subscription.objects.filter(admin1_ids__overlap=alert_admin1_ids)

    internal_alert = None
    updated_subscriptions = []

    with transaction.atomic():
        for subscription in subscriptions:
            matching_info = None

            for info in alert.capfeedalertinfo_set.all():
                if info.severity in subscription.severity_array and \
                        info.certainty in subscription.certainty_array and \
                        info.urgency in subscription.urgency_array:
                    matching_info = info
                    break

            if matching_info:
                if internal_alert is None:
                    internal_alert = Alert.objects.create(id=alert.id, serialised_string=json.dumps(
                        alert.to_dict()))

                updated_subscriptions.append(subscription)

                if subscription.sent_flag == 0:
                    process_immediate_alerts(subscription.id)

        if internal_alert:
            internal_alert.subscriptions.add(*updated_subscriptions)
            internal_alert.save()
            #Added alerts details to subscription alert cache
            for subscription in updated_subscriptions:
                cache_instance.cache_incoming_alert_for_subscription(subscription, internal_alert)
    cache_instance.update_cache()
    if updated_subscriptions:
        subscription_ids = [subscription.id for subscription in updated_subscriptions]
        return f"Incoming Alert {alert_id} is successfully converted. " \
               f"Mapped Subscription id are {subscription_ids}."

    return f"Incoming Alert {alert_id} is not mapped with any subscription."


#def formulate_serialised_

def delete_alert_to_subscription(alert_id):
    cache_instance = dynamic_cache()
    alert_to_be_deleted = Alert.objects.filter(id=alert_id).first()
    if alert_to_be_deleted is None:
        return f"Alert with id {alert_id} is not found in subscription database."

    subscriptions = alert_to_be_deleted.subscriptions.all()
    updated_subscription_ids = []
    for subscription in subscriptions:
        subscription.alert_set.remove(alert_to_be_deleted)
        # Update the cache when related alerts are removed
        cache_instance.cache_deleted_alert_for_subscription(subscription,alert_to_be_deleted)
        updated_subscription_ids.append(subscription.id)

    alert_to_be_deleted.delete()
    cache_instance.update_cache()

    if len(updated_subscription_ids) != 0:
        return f"Alert {alert_id} is successfully deleted from subscription database. " \
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

    map_subscription_to_alert(subscription)
    subscription_alerts_dict = subscription.subscription_alerts_to_dict()
    return json.dumps(subscription_alerts_dict, indent=None)
