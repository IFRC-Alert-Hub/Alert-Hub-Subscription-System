import asyncio
import signal
import sys
import threading

from django.core.management.base import BaseCommand, CommandError
import os
from django.http import HttpResponse

from subscription_manager_dir import establish_websockets_connection

class WebSocketThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.is_running = threading.Event()
        self.websocket_connection = establish_websockets_connection.WebsocketConnection()

    def run(self):
        while True:
            # Run the WebSocket connection
            try:
                self.websocket_connection.establish_websocket_connection()
                print("?")
                break
            except KeyboardInterrupt:  # pylint: disable=broad-except
                self.websocket_connection.close_connection()
                print("The connection is closed!")
                break
            except TimeoutError:
                print("This connection is timeout, retry the connection....")
            except ConnectionRefusedError:
                print("The connection is refused, retry the connection....")
            except ConnectionAbortedError:
                print("The connection is aborted, retry the connection....")


    def join(self, timeout=None):
        super().join(timeout)

class Command(BaseCommand):
    help = "Starting connections to " + os.environ.get("CAPAGGREGATOR_CONNECTION_WEBSITE") + "."

    def handle(self, *args, **options):
        print("?????")
        self.websocket_thread = WebSocketThread()
        self.websocket_thread.start()
        #self.websocket_thread.join()

        #Register the signal handler for keyboard interrupt
        signal.signal(signal.SIGINT, self.shutdown)

    def shutdown(self, signum, frame):
        print("Shutting down WebSocket connection...")
        self.websocket_thread.websocket_connection.close_connection()

