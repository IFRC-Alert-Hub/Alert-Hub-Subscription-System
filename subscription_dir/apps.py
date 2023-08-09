from django.apps import AppConfig
from subscription_manager_dir.subscription_alert_mapping import map_alert_to_subscription

class SubscriptionDirConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscription_dir'


