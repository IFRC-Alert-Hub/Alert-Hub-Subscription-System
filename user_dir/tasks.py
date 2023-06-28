from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from project import settings


@shared_task(bind=True)
def send_email(self, user_id, subject, template_name, context=None):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
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
