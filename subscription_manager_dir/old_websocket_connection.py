#Looking this file for old info
'''
import os
import threading
import json
import websocket

from django.http import HttpResponse

from subscription_dir.models import Subscription
from .tasks import send_subscription_email




def run_websocket():
    def on_message(message):
        # Process the received alert
        alert_map = json.loads(message)["message"]
        print(alert_map)
        matched_subscription = Subscription.objects.filter(
            country_ids__contains=[alert_map["country_id"]],
            urgency_array__contains=[alert_map["urgency"]],
            severity_array__contains=[alert_map["severity"]],
            certainty_array__contains=[alert_map["certainty"]]
        )
        for subscription in matched_subscription:
            context = {
                'country_name': alert_map["country_name"],
                'urgency': alert_map["urgency"],
                'severity': alert_map["severity"],
                'certainty': alert_map["certainty"],
            }
            print(context)
            try:
                send_subscription_email.delay(subscription.user_id,
                                              'New Alerts Matching Your Subscription',
                                              'subscription_email.html', context)
            except Exception as general_exception: # pylint: disable=broad-except
                print(f"Error: {general_exception}")

    def on_error(error):
        print(error)

    def on_close(close_status_code, close_msg):
        print(close_msg)

    # Create a WebSocket connection
    websocket.enableTrace(True)
    host_name = os.environ.get("CAPAGGREGATOR_CONNECTION_WEBSITE")
    web_socket = websocket.WebSocketApp(f"wss://{host_name}/ws/fetch_new_alert/1a/")

    # Set the callback function for incoming messages
    web_socket.on_message = on_message
    web_socket.on_error = on_error
    web_socket.on_close = on_close

    # Start the WebSocket connection
    web_socket.run_forever()


async def establish_connection_thread():
    # Run the WebSocket client in a separate thread
    websocket_thread = threading.Thread(target=run_websocket)
    websocket_thread.start()

    # Run the asyncio event loop in the main thread
    # while True:
    # Perform other asyncio-related tasks here if needed
    # await asyncio.sleep(1)

'''

