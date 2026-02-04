from django.contrib import admin
from .models import MedicalRecord, Report

# Register your models here.

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'record_date', 'created_at']
    list_filter = ['record_date']
    search_fields = ['patient__user_profile__user__username', 'diagnosis']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'patient', 'doctor', 'report_type', 'created_at']
    list_filter = ['report_type', 'created_at']
    search_fields = ['title', 'patient__user_profile__user__username']
