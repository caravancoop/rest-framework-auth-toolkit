from django.db import models


class BaseAPITokenManager(models.Manager):
    def create_token(self, user):
        return self.create(user=user)
