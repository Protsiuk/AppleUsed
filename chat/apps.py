from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = 'chat'
    verbose_name = _('Chat')

    def ready(self):
        import chat.signals