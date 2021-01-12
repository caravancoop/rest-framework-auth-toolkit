from django.urls import path

from .views import email_view


app_name = 'app-auth'

urlpatterns = [
    path('emails/<external_id>/', email_view, name='email-confirmation'),
]
