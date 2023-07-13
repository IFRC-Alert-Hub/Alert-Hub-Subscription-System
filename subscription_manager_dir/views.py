from django.http import HttpResponse

from .tasks import send_mail_fun

def send_mail_to_all(request):
    send_mail_fun.delay()
    return HttpResponse("Sent")
