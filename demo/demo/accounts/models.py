from django.contrib.auth.models import Group as BaseGroup
from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.fields import AutoCreatedField
from model_utils.models import TimeStampedModel
from shortuuidfield import ShortUUIDField

from rest_auth_toolkit.managers import BaseEmailUserManager
from rest_auth_toolkit.models import BaseEmailUser, BaseAPIToken, BaseEmailConfirmation


class UserManager(BaseEmailUserManager):
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


class User(BaseEmailUser):
    facebook_id = models.CharField(
        max_length=255, null=True, blank=True, help_text=_('FB third-party ID'))
    facebook_access_token = models.CharField(
        max_length=255, null=True, blank=True, help_text=_('FB access token'))

    objects = UserManager()


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
