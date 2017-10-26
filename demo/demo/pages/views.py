from django.conf import settings
from django.shortcuts import render
from django.utils.translation import gettext as _

from ..accounts.models import EmailConfirmation


def index(request):
    """Site root page."""
    ctx = {
        'site_name': 'Demo',
        'fb_app_id': settings.FACEBOOK_APP_ID,
    }
    return render(request, 'index.html', context=ctx)


def email_view(request, external_id):
    """Landing page for links in confirmation emails."""
    error = None

    try:
        confirmation = EmailConfirmation.objects.get(external_id=external_id)
        confirmation.confirm()
    except EmailConfirmation.DoesNotExist:
        error = _('Invalid link')
    except EmailConfirmation.IsExpired:
        error = _('Email expired, please register again')

    if error:
        ctx = {
            'site_name': 'Demo',
            'error': error,
        }
        return render(request, 'error.html', context=ctx)
    else:
        return index(request)
