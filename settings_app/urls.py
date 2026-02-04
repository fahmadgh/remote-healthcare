from django.urls import path
from . import views

app_name = 'settings_app'

urlpatterns = [
    path('user/', views.user_settings, name='user_settings'),
    path('change-password/', views.change_password, name='change_password'),
    path('system/', views.system_settings, name='system_settings'),
]
