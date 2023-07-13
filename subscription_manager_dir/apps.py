import os
import signal
import threading

from django.apps import AppConfig
from subscription_manager_dir.WebsocketThread import WebsocketThread


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
        if os.environ.get('RUN_MAIN') == 'true':
            current_thread = threading.current_thread()
            thread_name = current_thread.name
            thread_id = current_thread.ident
            print("Current Thread: Name={}, ID={}".format(thread_name, thread_id))
            signal.signal(signal.SIGINT, self.shutdown)
            self.websocket_thread = WebsocketThread()
            self.websocket_thread.start()

    def shutdown(self, signum, frame):
        self.websocket_thread.shutdown()
