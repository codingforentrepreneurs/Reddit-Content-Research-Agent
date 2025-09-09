from django.apps import AppConfig


class RedditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reddit'

    def ready(self):
        import reddit.signals # noqs