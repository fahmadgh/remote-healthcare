from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('doctor/', views.doctor_dashboard, name='doctor'),
    path('patient/', views.patient_dashboard, name='patient'),
]
