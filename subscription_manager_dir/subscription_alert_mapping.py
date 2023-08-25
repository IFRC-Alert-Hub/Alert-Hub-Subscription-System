import json

from django.db import transaction

from .cache import DynamicCache
from .external_alert_models import CapFeedAlert, CapFeedAdmin1
from .models import Subscription, SubscriptionAlerts, Alert
from .tasks import process_immediate_alerts


def map_subscriptions_to_alert():
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        map_subscription_to_alert(subscription)


def map_subscription_to_alert(subscription):
    #This stores alerts that are already processed.
    potential_alert_ids = []
    #This stores matched alerts.
    for admin1_id in subscription.admin1_ids:
        admin1 = CapFeedAdmin1.objects.filter(id=admin1_id).first()
        if admin1 is None:
            continue
        potential_alert_set = admin1.capfeedalert_set.all()

        for alert in potential_alert_set:
            if alert.id in potential_alert_ids:
                continue
            potential_alert_ids.append(alert.id)
            for info in alert.capfeedalertinfo_set.all():
                if info.severity in subscription.severity_array and \
                        info.certainty in subscription.certainty_array and \
                        info.urgency in subscription.urgency_array:

                    internal_alert = Alert.objects.filter(id=alert.id).first()
                    if internal_alert is None:
                        internal_alert = Alert.objects.create(id=alert.id)
                        internal_alert.save()
                    internal_alert.subscriptions.add(subscription)
                    break

def map_alert_to_subscription(alert_id):
    alert = CapFeedAlert.objects.filter(id=alert_id). \
        prefetch_related('admin1s', 'capfeedalertinfo_set').first()

    if alert is None:
        return f"Alert with id {alert_id} is not existed"

    converted_alert = Alert.objects.filter(id=alert_id).first()

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
                    internal_alert = Alert.objects.create(id=alert.id)

                updated_subscriptions.append(subscription)

                if subscription.sent_flag == 0:
                    process_immediate_alerts(subscription.id)

        if internal_alert:
            internal_alert.subscriptions.add(*updated_subscriptions)
            internal_alert.save()

    if updated_subscriptions:
        subscription_ids = [subscription.id for subscription in updated_subscriptions]
        return f"Incoming Alert {alert_id} is successfully converted. " \
               f"Mapped Subscription id are {subscription_ids}."

    return f"Incoming Alert {alert_id} is not mapped with any subscription."


def delete_alert_to_subscription(alert_id):
    alert_to_be_deleted = Alert.objects.filter(id=alert_id).first()
    if alert_to_be_deleted is None:
        return f"Alert with id {alert_id} is not found in subscription database."

    subscriptions = alert_to_be_deleted.subscriptions.all()
    updated_subscription_ids = []
    for subscription in subscriptions:
        subscription.alert_set.remove(alert_to_be_deleted)
        updated_subscription_ids.append(subscription.id)

    alert_to_be_deleted.delete()

    if len(updated_subscription_ids) != 0:
        return f"Alert {alert_id} is successfully deleted from subscription database. " \
               f"Updated Subscription id are " \
               f"{updated_subscription_ids}."

    return f"Alert {alert_id} is successfully deleted from subscription database. "

def get_subscription_alerts_without_mapping_records(subscription_id):
    subscription = Subscription.objects.filter(id=subscription_id).first()
    if subscription is None:
        return False

    map_subscription_to_alert(subscription)
    subscription_alerts_dict = subscription.get_alert_id_list()
    return json.dumps(subscription_alerts_dict, indent=None)
