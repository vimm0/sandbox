from django.apps import AppConfig


class CommentConfig(AppConfig):
    name = 'apps.comment'

    def ready(self):
        import apps.comment.signals  # noqa
