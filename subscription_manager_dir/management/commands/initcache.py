from django.core.management.base import BaseCommand
from subscription_manager_dir.subscription_alert_mapping import map_subscriptions_to_alert
from subscription_manager_dir.cache import cache_subscriptions_alert, clear_cache, \
    cache_subscriptions_admins
from django.core.cache import cache

class Command(BaseCommand):
    help = "Starting inputting alerts from alert database into subscription database"

    def handle(self, *args, **options):
        import time
        clear_cache()
        print("Clear Cache")

        # dict = {"8": {"id": 8, "event": "Marine Weather Statement", "category": "Met",
        #               "country_name": "Teyvat_1", "admin1s": ["Meng De"],
        #               "sent": "2023-08-22 21:40:59.514832+00:00"}
        #         }
        # alert_dict = {}
        # start_time = time.time()
        # for i in range(10000):
        #     list = []
        #     for j in range(200):
        #         list.append(dict)
        #     alert_dict[i] = list
        #     #cache.set("anything", list, timeout=None)
        # #print(f"time taken 1: {time.time() - start_time }")
        # cache.set("anything", alert_dict, timeout=None)
        # cache.get("anything")
        # print(f"time taken 2: {time.time() - start_time}")

