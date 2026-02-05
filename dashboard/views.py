from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from accounts.models import UserProfile, DoctorProfile, PatientProfile
from appointments.models import Appointment
from reports.models import MedicalRecord
from consultation.models import ConsultationNote
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.

@login_required
def home(request):
    """Main dashboard view - redirects based on user type"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        # User has profile - route based on user_type
        if user_profile.user_type == 'doctor':
            return doctor_dashboard(request)
        else:
            return patient_dashboard(request)
    except UserProfile.DoesNotExist:
        # No profile - check if admin/staff
        if request.user.is_superuser or request.user.is_staff:
            return redirect(reverse('admin:index'))
        else:
            # Regular user without profile - error state
            messages.error(request, 'Your user profile could not be loaded. This may indicate a system configuration issue. Please contact your system administrator for assistance.')
            logout(request)
            return redirect('accounts:login')


@login_required
def doctor_dashboard(request):
    """Doctor dashboard with scheduled appointments and patient info"""
    user_profile = UserProfile.objects.get(user=request.user)
    doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
    
    # Get today's and upcoming appointments
    today = timezone.now().date()
    upcoming_appointments = Appointment.objects.filter(
        doctor=doctor_profile,
        appointment_date__gte=today,
        status__in=['scheduled', 'confirmed']
    )[:10]
    
    # Get recent consultation notes
    recent_notes = ConsultationNote.objects.filter(doctor=doctor_profile)[:5]
    
    # Statistics
    total_appointments_today = Appointment.objects.filter(
        doctor=doctor_profile,
        appointment_date=today
    ).count()
    
    total_patients = Appointment.objects.filter(doctor=doctor_profile).values('patient').distinct().count()
    
    context = {
        'user_profile': user_profile,
        'doctor_profile': doctor_profile,
        'upcoming_appointments': upcoming_appointments,
        'recent_notes': recent_notes,
        'total_appointments_today': total_appointments_today,
        'total_patients': total_patients,
    }
    
    return render(request, 'dashboard/doctor_dashboard.html', context)


@login_required
def patient_dashboard(request):
    """Patient dashboard with appointments and medical history"""
    user_profile = UserProfile.objects.get(user=request.user)
    patient_profile = PatientProfile.objects.get(user_profile=user_profile)
    
    # Get upcoming appointments
    today = timezone.now().date()
    upcoming_appointments = Appointment.objects.filter(
        patient=patient_profile,
        appointment_date__gte=today,
        status__in=['scheduled', 'confirmed']
    )[:5]
    
    # Get recent medical records
    medical_history = MedicalRecord.objects.filter(patient=patient_profile)[:5]
    
    # Get past appointments
    past_appointments = Appointment.objects.filter(
        patient=patient_profile,
        status='completed'
    )[:5]
    
    context = {
        'user_profile': user_profile,
        'patient_profile': patient_profile,
        'upcoming_appointments': upcoming_appointments,
        'medical_history': medical_history,
        'past_appointments': past_appointments,
    }
    
    return render(request, 'dashboard/patient_dashboard.html', context)

