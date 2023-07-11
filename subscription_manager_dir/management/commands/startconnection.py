import asyncio
import sys

from django.core.management.base import BaseCommand, CommandError
import os
from django.http import HttpResponse

from subscription_manager_dir import establish_websockets_connection




class Command(BaseCommand):
    help = "Starting connections to " + os.environ.get("CAPAGGREGATOR_CONNECTION_WEBSITE") + "."

    def handle(self, *args, **options):
        while True:
            WebsocketConnection = establish_websockets_connection.WebsocketConnection()
            # Run the WebSocket connection
            try:
                asyncio.get_event_loop().run_until_complete(
                    WebsocketConnection.establish_websocket_connect())
                break
            except KeyboardInterrupt:  # pylint: disable=broad-except
                asyncio.ensure_future(WebsocketConnection.websocket.close())
                return "The connection is closed!"
            except TimeoutError:
                print("This connection is timeout, retry the connection....")

    def handle_interrupt(self, signum, frame):
        # Clean up tasks (if needed)
        print("Interrupt signal received. Stopping the command...")
        sys.exit(0)
