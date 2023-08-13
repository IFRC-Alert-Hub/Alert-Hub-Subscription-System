import os
import signal
from django.core.management.base import BaseCommand
from subscription_manager_dir.subscription_alert_mapping import map_subscriptions_to_alert
from subscription_manager_dir.cache import cache_subscriptions_alert

class Command(BaseCommand):
    help = "Starting inputting alerts from alert database into subscription database"

    def handle(self, *args, **options):
        # Converting all alerts in alert database into subscription database
        map_subscriptions_to_alert()
        print("All alerts data in alert database has been mapped with each subscription.")
        # Inputting all serialised alerts that maps each subscription into cache
        cache_subscriptions_alert()
        print("All alerts data that maps each subscriptions has been serialised and put into cache")



