"""demo URL Configuration."""

from django.urls import include, path
from django.contrib import admin

<<<<<<< HEAD
from rest_framework.documentation import include_docs_urls

from rest_auth_toolkit.views import FacebookLoginView, LoginView, LogoutView, SignupView
=======
from rest_auth_toolkit.views import (
    EmailConfirmationView,
    FacebookLoginView,
    LoginView,
    LogoutView,
    SignupView,
)
>>>>>>> 4eced4707f4c7b07cbbacd242e095ed010784349


auth_urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('confirm/', EmailConfirmationView.as_view(), name='confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('fb-login/', FacebookLoginView.as_view(), name='fb-login'),
]

api_urlpatterns = [
    path('account/', include('demo.accounts.urls')),
    path('', include_docs_urls(title='Demo API', permission_classes=[])),
    path('', include((auth_urlpatterns, 'auth'))),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
    path('', include('demo.pages.urls')),
]
