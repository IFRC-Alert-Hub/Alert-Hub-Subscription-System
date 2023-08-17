from django.http import HttpResponse
from .cache import get_subscription_alerts
from .subscription_alert_mapping import get_subscription_alerts_without_cache
def get_subscirption_alerts(request, subscription_id):
    result = get_subscription_alerts(subscription_id)
    if not result:
        return HttpResponse("Subscription is not found!", status=404)
    return HttpResponse(result)


def get_subscription_alerts_in_real_time(request, subscription_id):
    result = get_subscription_alerts_without_cache(subscription_id)
    if not result:
        return HttpResponse("Subscription is not found!", status=404)
    return HttpResponse(result)
