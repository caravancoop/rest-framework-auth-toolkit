from django.contrib.auth.models import AbstractUser, BaseUserManager, Group as BaseGroup
from django.db import models
from django.utils.translation import gettext_lazy as _

import shortuuid
from model_utils.fields import AutoCreatedField
from model_utils.models import TimeStampedModel
from shortuuidfield import ShortUUIDField

from rest_auth_toolkit.models import BaseAPIToken, BaseEmailConfirmation


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, email):
        return self.get(email=email)

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # XXX username is not automatically generated, don't understand why
        # (same model in another project works well!)
        if not user.username:
            user.username = str(shortuuid.uuid())
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields['is_staff']:
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields['is_superuser']:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_or_create_facebook_user(self, facebook_data, facebook_access_token):
        try:
            user = User.objects.get(email=facebook_data['email'])
        except User.DoesNotExist:
            user = self.create_user(
                email=facebook_data['email'],
                first_name=facebook_data['first_name'],
                last_name=facebook_data['last_name'],
                facebook_id=facebook_data['third_party_id'],
                facebook_access_token=facebook_access_token,
                is_active=True,
            )
            return user, True
        else:
            user.facebook_access_token = facebook_access_token
            user.save(update_fields=['facebook_access_token'])
            return user, False


class User(AbstractUser):
    """Custom user with email as login field."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Admin doesn't work well without username field; shortuuid provides
    # a simple way to get unique string values at creation time.
    username = ShortUUIDField()
    email = models.EmailField(max_length=255, unique=True)
    facebook_id = models.CharField(
        max_length=255, null=True, blank=True, help_text=_('FB third-party ID'))
    facebook_access_token = models.CharField(
        max_length=255, null=True, blank=True, help_text=_('FB access token'))

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email


class Group(BaseGroup):
    """Proxy model to have users and groups together in admin."""
    class Meta:
        proxy = True
        verbose_name = _('group')
        verbose_name_plural = _('groups')


class EmailConfirmation(BaseEmailConfirmation, TimeStampedModel):
    external_id = ShortUUIDField()


class APIToken(BaseAPIToken, models.Model):
    created = AutoCreatedField(_('created'))

    def revoke(self):
        self.delete()
