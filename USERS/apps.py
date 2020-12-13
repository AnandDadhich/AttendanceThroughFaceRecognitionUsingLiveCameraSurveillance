from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'USERS'

    def ready(self):
        import USERS.signals
