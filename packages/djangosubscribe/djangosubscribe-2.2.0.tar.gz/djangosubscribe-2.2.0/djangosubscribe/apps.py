from django.apps import AppConfig


class DjangosubscribeConfig(AppConfig):
    name = 'djangosubscribe'
    def ready(self):
        import djangosubscribe.signals