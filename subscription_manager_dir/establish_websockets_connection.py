import asyncio
import json

import websockets
import os
import logging

from subscription_dir.models import Subscription
from asgiref.sync import sync_to_async
from .tasks import send_subscription_email

# Enable trace logs
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


@sync_to_async
def filter_subscription(alert_map):
    return list(Subscription.objects.filter(
        country_ids__contains=[alert_map["country_id"]],
        urgency_array__contains=[alert_map["urgency"]],
        severity_array__contains=[alert_map["severity"]],
        certainty_array__contains=[alert_map["certainty"]]
    ))


async def process_incoming_alert(message):
    alert_map = json.loads(message)["message"]
    print(alert_map)
    matched_subscriptions = await filter_subscription(alert_map)


    for subscription in matched_subscriptions:
        context = {
            'country_name': alert_map["country_name"],
            'urgency': alert_map["urgency"],
            'severity': alert_map["severity"],
            'certainty': alert_map["certainty"],
        }
        print("b")
        try:
            send_subscription_email.delay(subscription.user_id,
                                          'New Alerts Matching Your Subscription',
                                          'subscription_email.html', context)
        except Exception as general_exception:  # pylint: disable=broad-except
            print(f"Error: {general_exception}")


async def establish_websocket_connect():
    host_name = os.environ.get("CAPAGGREGATOR_CONNECTION_WEBSITE")
    # Connect to the WebSocket server
    async with websockets.connect(f'wss://{host_name}/ws/fetch_new_alert/1a/',
                                  origin=os.environ.get("WEBSOCKET_ORIGIN")) as websocket:
        while True:
            try:
                message = await websocket.recv()
                await process_incoming_alert(message=message)
            except Exception as e:
                print(e)
                await websocket.close()
                break
