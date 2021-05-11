from django.apps import AppConfig
from django.db import models

from rest_framework.serializers import ModelSerializer


class AccountsConfig(AppConfig):
    name = 'demo.accounts'
    label = 'accounts'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from rest_auth_toolkit.fields import CustomEmailField

        ModelSerializer.serializer_field_mapping.update({
            models.EmailField: CustomEmailField,
        })
