import os

import websocket
from django.http import HttpResponse
from .tasks import send_mail_fun, send_subscription_email
from subscription_dir.models import Subscription
from user_dir.models import CustomUser
import json
def send_mail_to_all(request):
    send_mail_fun.delay()
    return HttpResponse("Sent")

import asyncio
import threading

#def send_packet(request):
#    asyncio.run(receive_messages())
#    return HttpResponse("Good")


def run_websocket():
    def on_message(ws, message):
        # Process the received alert
        alert_map = json.loads(message)["message"]
        print(alert_map)
        Matched_Subscription = Subscription.objects.filter(country_ids__contains=[alert_map["country_id"]],
                                                           urgency_array__contains=[alert_map["urgency"]],
                                                           severity_array__contains=[alert_map["severity"]],
                                                           certainty_array__contains=[alert_map["certainty"]]
                                                           )
        for subscription in Matched_Subscription:
            context = {
                'country_name': alert_map["country_name"],
                'urgency': alert_map["urgency"],
                'severity': alert_map["severity"],
                'certainty': alert_map["certainty"],
            }
            print(context)
            try:
                send_subscription_email.delay(subscription.user_id, 'New Alerts Matching Your Subscription', 'subscription_email.html', context)
            except Exception as e:
                print(f"Error: {e}")

    def on_error(ws, error):
        print(error)

    def on_close(ws, close_status_code, close_msg):
        print(close_msg)


    # Create a WebSocket connection
    websocket.enableTrace(True)
    host_name = os.environ.get("CAPAGGREGATOR_CONNECTION_WEBSITE")
    ws = websocket.WebSocketApp(f"wss://{host_name}/ws/fetch_new_alert/1a/")

    # Set the callback function for incoming messages
    ws.on_message = on_message
    ws.on_error = on_error
    ws.on_close = on_close


    # Start the WebSocket connection
    ws.run_forever()




async def main():
    # Run the WebSocket client in a separate thread
    websocket_thread = threading.Thread(target=run_websocket)
    websocket_thread.start()

    # Run the asyncio event loop in the main thread
    while True:
        # Perform other asyncio-related tasks here if needed
        await asyncio.sleep(1)
# Create your views here.
# Disable SSL certificate verification if needed
def receive_alert(request):
    # Run the asyncio event loop
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)