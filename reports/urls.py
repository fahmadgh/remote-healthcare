from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('medical-records/', views.medical_records_list, name='medical_records_list'),
    path('medical-records/<int:pk>/', views.medical_record_detail, name='medical_record_detail'),
    path('medical-records/create/', views.create_medical_record, name='create_medical_record'),
    path('', views.reports_list, name='reports_list'),
    path('generate/', views.generate_report, name='generate_report'),
    path('<int:pk>/', views.report_detail, name='report_detail'),
    path('<int:pk>/export-pdf/', views.export_report_pdf, name='export_pdf'),
    path('<int:pk>/export-csv/', views.export_report_csv, name='export_csv'),
]
