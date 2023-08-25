import json

from django.http import HttpResponse

from subscription_dir.models import Subscription
from .subscription_alert_mapping import get_subscription_alerts_without_mapping_records
def get_subscirption_alerts(request, subscription_id):
    try:
        subscription = Subscription.objects.get(id=subscription_id)
    except Subscription.DoesNotExist:
        return HttpResponse("Subscription is not found!", status=404)
    alert_list = subscription.get_alert_id_list()
    if len(alert_list) == 0:
        return HttpResponse("There is no alerts!", status=404)
    result = json.dumps(alert_list)
    return HttpResponse(result)


def get_subscription_alerts_in_real_time(request, subscription_id):
    result = get_subscription_alerts_without_mapping_records(subscription_id)
    if not result:
        return HttpResponse("Subscription is not found!", status=404)
    return HttpResponse(result)
