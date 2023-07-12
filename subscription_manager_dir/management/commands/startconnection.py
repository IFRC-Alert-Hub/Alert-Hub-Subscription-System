import asyncio
import signal
import sys
import threading

import websockets.exceptions
from django.core.management.base import BaseCommand, CommandError
import os
from django.http import HttpResponse

from subscription_manager_dir.establish_websockets_connection import WebsocketConnection


class WebSocketThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.is_running = threading.Event()
        self.websocket_connection = WebsocketConnection()

    def run(self):
        while True:
            # Run the WebSocket connection
            try:
                self.websocket_connection.establish_websocket_connection()
                break
            except KeyboardInterrupt:  # pylint: disable=broad-except
                self.websocket_connection.close_connection()
                print("The connection is closed!")
                break
            except TimeoutError:
                print("This connection is timeout, retry the connection....")
                WebsocketConnection.isConnected(False)
            except ConnectionRefusedError:
                print("The connection is refused, retry the connection....")
                WebsocketConnection.isConnected(False)
            except ConnectionAbortedError:
                print("The connection is aborted, retry the connection....")
                WebsocketConnection.isConnected(False)
            except websockets.exceptions.InvalidStatus:
                print("The connection is rejected, retry the connection....")
                WebsocketConnection.isConnected(False)
            except websockets.exceptions.ConnectionClosedOK:
                print("The connection is successfully closed.")
                WebsocketConnection.isConnected(False)
                break

    def stop(self):
        self.is_running.clear()

    def join(self, timeout=None):
        super().join(timeout)

class Command(BaseCommand):
    help = "Starting connections to " + os.environ.get("CAPAGGREGATOR_CONNECTION_WEBSITE") + "."

    def handle(self, *args, **options):
        # Register the signal handler for keyboard interrupt
        signal.signal(signal.SIGINT, self.shutdown)
        self.websocket_thread = WebSocketThread()
        self.websocket_thread.start()

    def shutdown(self, signum, frame):
        if self.websocket_thread.websocket_connection.checkConnected():
            print("Shutting down WebSocket connection...")
            self.websocket_thread.websocket_connection.close_connection()
            self.websocket_thread.stop()
        exit(0)

