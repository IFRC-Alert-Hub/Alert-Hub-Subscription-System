import asyncio
import signal
import sys
import threading

import websockets.exceptions
from django.core.management.base import BaseCommand, CommandError
import os
from django.http import HttpResponse

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

