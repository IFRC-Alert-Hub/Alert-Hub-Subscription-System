# pylint: disable=R0801
from collections import defaultdict
from datetime import timedelta

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
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=True,
    )

    return "Done"


@shared_task
def process_non_immediate_alerts(sent_flag):
    from .models import Subscription, SubscriptionAlerts

    user = get_user_model()
    subscriptions = Subscription.objects.filter(sent_flag=sent_flag)

    for subscription in subscriptions:
        subscription_id = subscription.id
        subscription_name = subscription.subscription_name
        user_id = subscription.user_id

        related_alerts = SubscriptionAlerts.objects.filter(subscription=subscription_id, sent=False)

        if not related_alerts:
            continue

        related_alerts_count = related_alerts.count()

        viewer_link = "https://alert-hub-frontend.azurewebsites.net/"

        context = {
            'title': subscription_name,
            'count': related_alerts_count,
            'viewer_link': viewer_link,
        }

        send_subscription_email.delay(user_id, 'New Alerts Matching Your Subscription',
                                      'non_immediate_alerts_email.html', context)

        related_alerts.update(sent=True)


@shared_task
def get_incoming_alert(alert_id):
    pass


@shared_task
def get_removed_alert(alert_id):
    pass
