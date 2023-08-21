from django.core.management.base import BaseCommand
from subscription_manager_dir.cache import clear_cache, cache_subscriptions_admins


class Command(BaseCommand):
    help = "Starting inputting alerts from alert database into subscription database"

    def handle(self, *args, **options):
        clear_cache()
        print("Clear Cache")
        cache_subscriptions_admins()
        print("All admin ids that has corresponding subscriptions has been cached")
