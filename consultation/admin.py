from django.contrib import admin
from .models import ConsultationNote, ChatMessage, VideoSession

# Register your models here.

@admin.register(ConsultationNote)
class ConsultationNoteAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'doctor', 'patient', 'created_at']
    list_filter = ['created_at']
    search_fields = ['patient__user_profile__user__username', 'diagnosis']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'sender', 'timestamp', 'is_read']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['sender__username', 'message']

@admin.register(VideoSession)
class VideoSessionAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'status', 'start_time', 'end_time', 'duration_minutes']
    list_filter = ['status']
