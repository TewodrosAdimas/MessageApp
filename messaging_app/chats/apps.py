from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chats"

class ChatAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chats"

    def ready(self):
        import chats.signals