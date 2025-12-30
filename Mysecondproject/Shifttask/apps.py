from django.apps import AppConfig



class ShifttaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Shifttask'

    def ready(self):
        import Shifttask.signals
