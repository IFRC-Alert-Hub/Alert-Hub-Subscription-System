from django.http import HttpResponse
from .cache import get_subscription_alerts

def get_subscirption_alerts(request, subscription_id):
    result = get_subscription_alerts(subscription_id)
    if not result:
        return HttpResponse("Subscription is not found!", status=404)
    return HttpResponse(get_subscription_alerts(subscription_id))
