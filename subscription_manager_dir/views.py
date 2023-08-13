from django.http import HttpResponse
from .tasks import send_mail_fun
from django.core.cache import cache
from .cache import get_subscription_alerts
def send_mail_to_all(request):
    send_mail_fun.delay()
    return HttpResponse("Sent")

def get_subscirption_alerts(request, subscription_id):
    return HttpResponse(get_subscription_alerts(subscription_id))