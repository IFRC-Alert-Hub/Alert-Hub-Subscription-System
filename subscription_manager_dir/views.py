from django.http import HttpResponse
from .cache import get_subscription_alerts

def get_subscirption_alerts(request, subscription_id):
    return HttpResponse(get_subscription_alerts(subscription_id))
