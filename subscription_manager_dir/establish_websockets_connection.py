import json
import logging
import os

from websockets.sync.client import connect
from .tasks import send_subscription_email


class WebsocketConnection:
    connected = False

    def __init__(self):
        self.websocket = None
        # Configure logging settings
        logging.basicConfig(level=logging.INFO)

        # Create a logger instance
        self.logger = logging.getLogger(__name__)

    def filter_subscription(self, alert_map):
        from subscription_dir.models import Subscription
        return list(Subscription.objects.filter(
            country_ids__contains=[alert_map["country_id"]],
            urgency_array__contains=[alert_map["urgency"]],
            severity_array__contains=[alert_map["severity"]],
            certainty_array__contains=[alert_map["certainty"]]
        ))

    def process_incoming_alert(self, message):
        alert_map = json.loads(message)["message"]
        print(alert_map)
        matched_subscriptions = self.filter_subscription(alert_map)

        for subscription in matched_subscriptions:
            context = {
                'country_name': alert_map["country_name"],
                'urgency': alert_map["urgency"],
                'severity': alert_map["severity"],
                'certainty': alert_map["certainty"],
            }
            try:
                send_subscription_email.delay(subscription.user_id,
                                              'New Alerts Matching Your Subscription',
                                              'subscription_email.html', context)
            except Exception as general_exception:  # pylint: disable=broad-except
                print(f"Error: {general_exception}")

    @classmethod
    def isConnected(cls, bool):
        cls.connected = bool

    @classmethod
    def checkConnected(cls):
        return cls.connected

    def establish_websocket_connection(self):
        if WebsocketConnection.checkConnected():
            self.logger.info("The websocket connection is already established!")
            return None
        host_name = os.environ.get("CAPAGGREGATOR_CONNECTION_WEBSITE")
        # Connect to the WebSocket server
        with connect(f'{host_name}/ws/fetch_new_alert/1a/',
                     origin=os.environ.get("WEBSOCKET_ORIGIN")) as websocket:
            WebsocketConnection.isConnected(True)
            self.websocket = websocket
            self.logger.info("Connection Established!")
            while True:
                message = websocket.recv()
                self.logger.info("Received: " + message)
                self.process_incoming_alert(message=message)

    def close_connection(self):
        if self.websocket:
            self.isConnected(False)
            self.websocket.close()
