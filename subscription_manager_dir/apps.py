import logging
import os
import signal
import threading

from django.apps import AppConfig
from subscription_manager_dir.websocket_thread import WebsocketThread


class SubscriptionManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscription_manager_dir'
    connected = False

    @classmethod
    def is_connected(cls):
        cls.connected = True

    @classmethod
    def check_connected(cls):
        return cls.connected

    def ready(self):
        # Configure logging settings
        logging.basicConfig(level=logging.INFO)
        # Create a logger instance
        logger = logging.getLogger(__name__)
        logger.info("Trying Establishing the Websocket Connection...")
        if os.environ.get('RUN_MAIN') == 'true' or os.environ.get('RUN_MAIN') == None:
            logger.info("Really?")
            current_thread = threading.current_thread()
            thread_name = current_thread.name
            thread_id = current_thread.ident
            print(f"Current Thread: Name={thread_name}, ID={thread_id}")
            signal.signal(signal.SIGINT, self.shutdown)
            self.websocket_thread = WebsocketThread()
            self.websocket_thread.start()

    def shutdown(self, signum, frame):
        self.websocket_thread.shutdown()
