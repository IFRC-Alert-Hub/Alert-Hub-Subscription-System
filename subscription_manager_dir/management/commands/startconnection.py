import os
import signal
from django.core.management.base import BaseCommand
from subscription_manager_dir.WebsocketThread import WebsocketThread


class Command(BaseCommand):
    help = "Starting connections to " + os.environ.get("CAPAGGREGATOR_CONNECTION_WEBSITE") + "."

    def handle(self, *args, **options):
        # Register the signal handler for keyboard interrupt
        signal.signal(signal.SIGINT, self.shutdown)
        self.websocket_thread = WebsocketThread()
        self.websocket_thread.start()

    def shutdown(self, signum, frame):
        self.websocket_thread.shutdown()
