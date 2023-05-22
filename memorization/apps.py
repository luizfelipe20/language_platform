from django.apps import AppConfig


class MemorizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'memorization'

    def ready(self):
       import memorization.signals  # noqa
