from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SystemSettings(models.Model):
    """System-wide settings"""
    setting_key = models.CharField(max_length=100, unique=True)
    setting_value = models.TextField()
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "System Settings"
    
    def __str__(self):
        return self.setting_key


class UserSettings(models.Model):
    """User-specific settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    
    # Privacy settings
    profile_visibility = models.BooleanField(default=True)
    show_phone = models.BooleanField(default=False)
    show_email = models.BooleanField(default=True)
    
    # Theme preferences
    theme = models.CharField(max_length=20, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    
    # Communication preferences
    allow_messages = models.BooleanField(default=True)
    allow_video_calls = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Settings - {self.user.username}"

