# pylint: disable=R0801
from collections import defaultdict

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .subscription_alert_mapping import map_subscriptions_to_alert, map_alert_to_subscription, delete_alert_to_subscription
from .cache import cache_subscriptions_alert
from celery import shared_task

from project import settings


@shared_task(bind=True)
def send_mail_fun(self):
    users = get_user_model().objects.all()
    for user in users:
        mail_subject = "xxx"
        message = "xxxxx"
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "Done"


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
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=True,
    )

    return "Done"

'''
@shared_task
def process_non_immediate_alerts():
    #from .models import Alerts
    #users = get_user_model().objects.all()
    #alerts = Alerts.objects.filter(is_sent=False).select_related('user')
    #user_alerts = defaultdict(list)

    # Group alerts by user
    for alert in alerts:
        user_alerts[alert.user_id].append(alert)

    # Send email to each user with their alerts
    for user in users:
        if user.id in user_alerts:
            alerts_for_user = []
            for alert in user_alerts[user.id]:
                alerts_for_user.append({
                    'id': alert.id,
                    'country_name': alert.country_name,
                    'country_id': alert.country_id,
                    'source_feed': alert.source_feed,
                    'scope': alert.scope,
                    'urgency': alert.urgency,
                    'severity': alert.severity,
                    'certainty': alert.certainty,
                    'info': alert.info,
                    'created_at': alert.created_at,
                })
            context = {
                'alerts': alerts_for_user,
            }
            send_subscription_email.delay(user.id, 'New Alerts Matching Your Subscription',
                                          'non_immediate_alerts_email.html', context)
            Alerts.objects.filter(id__in=[alert.id for alert in user_alerts[user.id]]).update(
                is_sent=True)
'''
@shared_task
def get_incoming_alert(alert_id):
    return map_alert_to_subscription(alert_id)

@shared_task
def get_removed_alert(alert_id):
    return delete_alert_to_subscription(alert_id)

@shared_task
def initialise_task():
    map_subscriptions_to_alert()
    cache_subscriptions_alert()