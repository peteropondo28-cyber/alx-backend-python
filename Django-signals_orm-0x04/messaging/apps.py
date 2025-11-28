from django.apps import AppConfig


class MessagingConfig(AppConfig):
    name = 'messaging'
    verbose_name = "Messaging App"

    def ready(self):
        # Import signals module to ensure signal handlers are connected
        import messaging.signals  # noqa: F401
