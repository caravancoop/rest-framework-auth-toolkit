from django.conf.urls import url

from . import views


app_name = 'pages'


urlpatterns = [
    url(r'^$', views.index, name='root'),
    url(r'^welcome/(?P<token>[^/.]+)$', views.confirm_email, name='confirm-email'),
]
