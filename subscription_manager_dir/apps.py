import logging
import os
import signal
import sys
import threading
import random
import time
from django.core.cache import cache

from django.apps import AppConfig


class SubscriptionManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscription_manager_dir'

    def ready(self):
        if 'WEBSITE_HOSTNAME' in os.environ or \
            ('WEBSITE_HOSTNAME' not in os.environ and 'runserver' in sys.argv):
            from .subscription_alert_mapping import map_subscriptions_to_alert,print_all_admin1s_in_country
            result = cache.add('locked', True, timeout=10)
            if result:
                map_subscriptions_to_alert()
                print_all_admin1s_in_country(161)
