import logging
import os
import signal
import sys
import threading
import random
import time

from django.apps import AppConfig
from django.db.models.signals import post_save
from django.core.cache import cache



class SubscriptionManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscription_manager_dir'

    def ready(self):
        if 'WEBSITE_HOSTNAME' in os.environ or \
            ('WEBSITE_HOSTNAME' not in os.environ and 'runserver' in sys.argv):
            #from .subscription_alert_mapping import map_alerts_to_subscription
            #from .cache import cache_subscriptions_alert
            result = cache.add('locked', True, timeout=5)
            if result:
                pass
                #map_alerts_to_subscription()
                #cache_subscriptions_alert()

