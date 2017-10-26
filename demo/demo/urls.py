"""demo URL Configuration."""

from django.conf.urls import url, include
from django.contrib import admin

from rest_auth_toolkit.views import FacebookLoginView, LoginView, LogoutView, SignupView


auth_urlpatterns = [
    url(r'^signup/', SignupView.as_view(), name='signup'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^fb-login/', FacebookLoginView.as_view(), name='fb-login'),
]

api_urlpatterns = [
    url(r'^account/', include('demo.accounts.urls')),
    url(r'', include((auth_urlpatterns, 'auth'))),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_urlpatterns)),
    url(r'', include('demo.pages.urls')),
    url(r'', include('demo.pages.auth_urls')),
]
