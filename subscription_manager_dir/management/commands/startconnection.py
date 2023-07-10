import asyncio

from django.core.management.base import BaseCommand, CommandError
import os

from django.http import HttpResponse

from subscription_manager_dir.websocket_connection import establish_connection_thread
class Command(BaseCommand):
    help = "Starting connections to " + os.environ.get("CAPAGGREGATOR_CONNECTION_WEBSITE") + "."

    def handle(self, *args, **options):
        while True:
            try:
                asyncio.run(establish_connection_thread())
                break
            except Exception as general_exception:  # pylint: disable=broad-except
                print(general_exception)
                return HttpResponse("An error occurred.")
