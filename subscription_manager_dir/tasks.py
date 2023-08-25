# pylint: disable=R0801
import json

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from celery import shared_task
from project import settings


@shared_task(bind=True)
def send_subscription_email(self, user_id, subject, template_name, context=None):
    custom_user = get_user_model()
    try:
        user = custom_user.objects.get(id=user_id)
    except custom_user.DoesNotExist:
        return "Invalid User ID"

    context = context or {}
    context.update({
        'user': user,
    })

    message = render_to_string(template_name, context)

    send_mail(
        subject=subject,
        message=strip_tags(message),
        html_message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )

    return "Done"


@shared_task
def process_immediate_alerts(subscription_id):
    from .models import Subscription, SubscriptionAlerts

    subscription = Subscription.objects.get(id=subscription_id)

    subscription_name = subscription.subscription_name
    user_id = subscription.user_id

    related_alerts = SubscriptionAlerts.objects.filter(subscription=subscription_id, sent=False)

    if not related_alerts:
        return

    related_alerts_count = related_alerts.count()

    alert_info = []
    for related_alert in related_alerts:
        alert = related_alert.alert
        #alert_details = json.loads(alert.serialised_string)
        #alert_info.append(alert_details)

    viewer_link = "https://alert-hub-frontend.azurewebsites.net/account/subscription"

    context = {
        'title': subscription_name,
        'count': related_alerts_count,
        'viewer_link': viewer_link,
        'alerts': alert_info,
    }

    send_subscription_email.delay(user_id, '[IFRC] New alert update from your subscriptions',
                                  'subscription_email.html', context)

    related_alerts.update(sent=True)


@shared_task
def process_non_immediate_alerts(sent_flag):
    from .models import Subscription, SubscriptionAlerts

    subscriptions = Subscription.objects.filter(sent_flag=sent_flag)

    for subscription in subscriptions:
        subscription_id = subscription.id
        subscription_name = subscription.subscription_name
        user_id = subscription.user_id

        related_alerts = SubscriptionAlerts.objects.filter(subscription=subscription_id, sent=False)

        if not related_alerts:
            continue

        related_alerts_count = related_alerts.count()

        viewer_link = "https://alert-hub-frontend.azurewebsites.net/account/subscription"

        context = {
            'title': subscription_name,
            'count': related_alerts_count,
            'viewer_link': viewer_link,
        }

        send_subscription_email.delay(user_id, 'New Alerts Matching Your Subscription',
                                      'subscription_email.html', context)

        related_alerts.update(sent=True)


@shared_task
def get_incoming_alert(alert_id):
    from .subscription_alert_mapping import map_alert_to_subscription
    return map_alert_to_subscription(alert_id)


@shared_task
def get_removed_alert(alert_id):
    from .subscription_alert_mapping import delete_alert_to_subscription
    return delete_alert_to_subscription(alert_id)


@shared_task
def initialise_task():
    from .subscription_alert_mapping import map_subscriptions_to_alert
    map_subscriptions_to_alert()
