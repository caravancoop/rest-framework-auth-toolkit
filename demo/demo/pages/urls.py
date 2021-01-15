from django.urls import path

from . import views


app_name = 'pages'


urlpatterns = [
    path('', views.index, name='root'),
    path('welcome/<token>/', views.confirm_email, name='confirm-email'),
]
