from django.contrib import admin
from .models import SystemSettings, UserSettings

# Register your models here.

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['setting_key', 'setting_value', 'updated_at']
    search_fields = ['setting_key', 'description']

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'profile_visibility', 'updated_at']
    list_filter = ['theme', 'profile_visibility']
