import asyncio
from django.http import HttpResponse
from websocket_connection import establish_connection_thread

# Create your views here.
# Disable SSL certificate verification if needed
def receive_alert(request):
    try:
        asyncio.run(establish_connection_thread())
    except Exception as general_exception:  # pylint: disable=broad-except
        print(general_exception)
        return HttpResponse("An error occurred.")

    return HttpResponse("Good!")
