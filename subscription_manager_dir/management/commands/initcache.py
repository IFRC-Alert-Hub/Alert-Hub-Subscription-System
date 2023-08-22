from django.core.management.base import BaseCommand
from subscription_manager_dir.subscription_alert_mapping import map_subscriptions_to_alert
from subscription_manager_dir.cache import cache_subscriptions_alert, clear_cache, \
    cache_subscriptions_admins


class Command(BaseCommand):
    help = "Starting inputting alerts from alert database into subscription database"

    def handle(self, *args, **options):
        clear_cache()
        print("Clear Cache")
