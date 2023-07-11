import asyncio
import sys

from django.core.management.base import BaseCommand, CommandError
import os
from django.http import HttpResponse

from subscription_manager_dir.establish_websockets_connection import establish_websocket_connect
class Command(BaseCommand):
    help = "Starting connections to " + os.environ.get("CAPAGGREGATOR_CONNECTION_WEBSITE") + "."

    def handle(self, *args, **options):
        while True:
            try:
                # Run the WebSocket connection
                asyncio.get_event_loop().run_until_complete(establish_websocket_connect())
                break
            except Exception as general_exception:  # pylint: disable=broad-except
                print(general_exception)
                return 'Failed'

    def handle_interrupt(self, signum, frame):
        # Clean up tasks (if needed)
        print("Interrupt signal received. Stopping the command...")
        sys.exit(0)
