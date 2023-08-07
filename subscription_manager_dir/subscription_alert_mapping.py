from .external_alert_models import *
from subscription_dir.models import Subscription
from .models import *
def map_alerts_to_subscription():
    for subscription in Subscription.objects.all():
        if not hasattr(subscription, 'subscriptionalerts'):
            map_alert_to_subscription(subscription)
        else:
            pass


def map_alert_to_subscription(subscription):
    alert_ids = []
    for id in subscription.district_ids:
        admin1 = CapFeedAdmin1.objects.using('AlertDB').filter(id=id).first()
        potential_alert_set = admin1.capfeedalert_set.all()

        for alert in potential_alert_set:
            first_info = alert.capfeedalertinfo_set.first()
            if first_info.severity in subscription.severity_array and \
            first_info.certainty in subscription.certainty_array and \
            first_info.urgency in subscription.urgency_array:
                alert_ids.append(alert.id)

    SubscriptionAlerts.objects.create(alert_ids=alert_ids,subscription=subscription).save()

def print_all_admin1s_in_country(id):
    ids = []
    admin1s = CapFeedAdmin1.objects.using('AlertDB').filter(country__id=id)
    for admin in admin1s:
        ids.append(admin.id)