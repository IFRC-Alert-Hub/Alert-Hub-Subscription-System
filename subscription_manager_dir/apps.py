from django.apps import AppConfig
from django.core import management

class SubscriptionManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscription_manager_dir'
    connected = False

    @classmethod
    def isConnected(cls):
        cls.connected = True

    @classmethod
    def checkConnected(cls):
        return cls.connected

    def ready(self):
        if not self.__class__.checkConnected():
            management.call_command('startconnection')
            self.__class__.isConnected()


