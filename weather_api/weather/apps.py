from django.apps import AppConfig


class WeatherConfig(AppConfig):
    """
    App configuration for the 'weather' application.

    This class sets the default auto field type for models in the app to 'BigAutoField'
    and specifies the app's name as 'weather'. It is used by Django to configure
    application-specific settings.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'
