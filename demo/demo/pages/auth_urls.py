from django.conf.urls import url

from .views import email_view


app_name = 'app-auth'

urlpatterns = [
    url(r'^emails/(?P<external_id>[^/.]+)$', email_view, name='email-confirmation'),
]
