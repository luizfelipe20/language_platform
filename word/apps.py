from django.apps import AppConfig


class WordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # default_auto_field = 'language_platform.word'
    name = 'word'

    def ready(self):
       ... 