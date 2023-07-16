import logging
import os
import signal
import sys
import threading
import random
import time
from django.core.cache import cache

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
        if os.environ.get('WEBSOCKET_CONNECTION', False) \
                and 'migrate' not in sys.argv \
                and 'runserver' in sys.argv:
            print("True")
            # Generate a random delay in milliseconds (0 to 5000 ms)
            delay_ms = random.randint(0, 5000)
            # Convert milliseconds to seconds (1 second = 1000 milliseconds)
            delay_seconds = delay_ms / 1000.0
            time.sleep(delay_seconds)

            # Configure logging settings
            logging.basicConfig(level=logging.INFO)
            # Create a logger instance
            logger = logging.getLogger(__name__)
            logger.info("Trying Establishing the Websocket Connection...")
            if cache.get('connected') == None:
                cache.set('connected', 'True', timeout=20)
                current_thread = threading.current_thread()
                thread_name = current_thread.name
                thread_id = current_thread.ident
                print(f"Current Thread: Name={thread_name}, ID={thread_id}")
                signal.signal(signal.SIGINT, self.shutdown)
                self.websocket_thread = WebsocketThread()
                self.websocket_thread.start()

    def shutdown(self, signum, frame):
        self.websocket_thread.shutdown()
