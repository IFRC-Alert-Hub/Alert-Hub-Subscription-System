import os
import asyncio
from .old_websocket_connection import establish_connection_thread
from django.http import HttpResponse

from .tasks import send_mail_fun

def send_mail_to_all(request):
    send_mail_fun.delay()
    return HttpResponse("Sent")

# Create your views here.
# Disable SSL certificate verification if needed
def receive_alert(request):
    try:
        asyncio.run(establish_connection_thread())
    except Exception as general_exception:  # pylint: disable=broad-except
        print(general_exception)
        return HttpResponse("An error occurred.")

    return HttpResponse("Good!")
