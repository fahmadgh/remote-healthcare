from django.contrib import admin
from .models import UserProfile, DoctorProfile, PatientProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone_number', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'specialization', 'license_number', 'available']
    list_filter = ['specialization', 'available']
    search_fields = ['user_profile__user__username', 'license_number']

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'blood_group', 'emergency_contact']
    search_fields = ['user_profile__user__username', 'emergency_contact_name']
