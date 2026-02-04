from django.db import models
from accounts.models import PatientProfile, DoctorProfile
from appointments.models import Appointment

# Create your models here.

class ConsultationNote(models.Model):
    """Consultation notes during appointments"""
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='consultation_notes')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='consultation_notes')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='consultation_notes')
    
    chief_complaint = models.TextField()
    history = models.TextField(blank=True)
    examination = models.TextField(blank=True)
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    follow_up = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Consultation Note - {self.appointment}"


class ChatMessage(models.Model):
    """Chat messages between doctor and patient"""
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"


class VideoSession(models.Model):
    """Video consultation sessions"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='video_session')
    session_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Video Session - {self.appointment}"

