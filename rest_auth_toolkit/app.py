from django.apps import AppConfig


class RestAuthToolkitConfig(AppConfig):
    """Default app config for RATK.

    This installs a signal handler to set user.is_active when
    email_confirmed is emitted.
    """
    name = 'rest_auth_toolkit'
    default = True

    def ready(self):
        from .models import email_confirmed
        from .views import activate_user
        email_confirmed.connect(activate_user)


class RestAuthToolkitMinimalConfig(AppConfig):
    """App config without signal handler setup.

    Use this when you don't want to set user.is_active when
    email_confirmed is emitted.
    """
    name = 'rest_auth_toolkit'
