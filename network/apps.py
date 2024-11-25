from django.apps import AppConfig


class NetworkConfig(AppConfig):
    name = 'network'
    default_auto_field = 'django.db.models.BigAutoField'

class NotificationConfig(AppConfig):
    name = 'notification'