from django.apps import AppConfig

class IdentitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.identities'

    def ready(self):
        import apps.identities.signals