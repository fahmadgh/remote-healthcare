from django.db import models
from accounts.models import PatientProfile, DoctorProfile
from appointments.models import Appointment

# Create your models here.

class MedicalRecord(models.Model):
    """Patient medical records"""
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, related_name='created_records')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='records')
    
    diagnosis = models.TextField()
    symptoms = models.TextField()
    prescription = models.TextField()
    lab_results = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    record_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-record_date', '-created_at']
    
    def __str__(self):
        return f"{self.patient} - {self.record_date}"


class Report(models.Model):
    """Consultation reports"""
    REPORT_TYPE_CHOICES = [
        ('consultation', 'Consultation Summary'),
        ('prescription', 'Prescription'),
        ('lab', 'Lab Report'),
        ('medical_history', 'Medical History'),
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='reports')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, related_name='generated_reports')
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    file_path = models.FileField(upload_to='reports/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.patient}"

