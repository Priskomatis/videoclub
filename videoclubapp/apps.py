from django.apps import AppConfig



class VideoclubappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videoclubapp'

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "users"

    def ready(self):
        import videoclubapp.signals