import os
import sys

from django.apps import AppConfig


class SubscriptionManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscription_manager_dir'

    def ready(self):
        if ('WEBSITE_HOSTNAME' in os.environ and 'migrate' not in sys.argv and 'collectstatic'
            not in sys.argv) \
                or \
                ('WEBSITE_HOSTNAME' not in os.environ and 'runserver' in sys.argv):
            from django.core.cache import cache
            result = cache.add('locked', True, timeout=60)
            if result:
                pass
                # from .subscription_alert_mapping import map_alerts_to_subscription
                # from .cache import cache_subscriptions_alert
                # map_alerts_to_subscription()
                # cache_subscriptions_alert()
