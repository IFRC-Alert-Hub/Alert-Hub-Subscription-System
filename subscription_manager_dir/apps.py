from django.apps import AppConfig
from django.core import management

class SubscriptionManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscription_manager_dir'

    def ready(self):
        print("?????????")
        # Your initialization or startup code here
        management.call_command('startconnection')


