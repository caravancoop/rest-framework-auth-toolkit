from django.conf.urls import url

from .views import ProfileView


urlpatterns = [
    url(r'', ProfileView.as_view(), name='user-profile'),
]
