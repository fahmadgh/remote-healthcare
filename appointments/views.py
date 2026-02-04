from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.models import UserProfile, DoctorProfile, PatientProfile
from .models import Appointment, DoctorAvailability

# Create your views here.

@login_required
def appointment_list(request):
    """List all appointments for the current user"""
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.user_type == 'doctor':
        doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
        appointments = Appointment.objects.filter(doctor=doctor_profile)
    else:
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        appointments = Appointment.objects.filter(patient=patient_profile)
    
    context = {
        'appointments': appointments,
        'user_profile': user_profile,
    }
    return render(request, 'appointments/appointment_list.html', context)


@login_required
def book_appointment(request):
    """Book a new appointment"""
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.user_type != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('dashboard:home')
    
    patient_profile = PatientProfile.objects.get(user_profile=user_profile)
    doctors = DoctorProfile.objects.filter(available=True)
    
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')
        
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)
        
        # Check if the time slot is available
        existing_appointment = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status__in=['scheduled', 'confirmed']
        ).exists()
        
        if existing_appointment:
            messages.error(request, 'This time slot is already booked. Please choose another time.')
            return render(request, 'appointments/book_appointment.html', {'doctors': doctors})
        
        # Create appointment
        appointment = Appointment.objects.create(
            patient=patient_profile,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            status='scheduled'
        )
        
        messages.success(request, 'Appointment booked successfully! You will receive a confirmation soon.')
        return redirect('appointments:appointment_detail', pk=appointment.id)
    
    context = {
        'doctors': doctors,
        'user_profile': user_profile,
    }
    return render(request, 'appointments/book_appointment.html', context)


@login_required
def appointment_detail(request, pk):
    """View appointment details"""
    appointment = get_object_or_404(Appointment, pk=pk)
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check if user has permission to view this appointment
    if user_profile.user_type == 'doctor':
        doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
        if appointment.doctor != doctor_profile:
            messages.error(request, 'You do not have permission to view this appointment.')
            return redirect('dashboard:home')
    else:
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        if appointment.patient != patient_profile:
            messages.error(request, 'You do not have permission to view this appointment.')
            return redirect('dashboard:home')
    
    context = {
        'appointment': appointment,
        'user_profile': user_profile,
    }
    return render(request, 'appointments/appointment_detail.html', context)


@login_required
def cancel_appointment(request, pk):
    """Cancel an appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check permissions
    if user_profile.user_type == 'patient':
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        if appointment.patient != patient_profile:
            messages.error(request, 'You do not have permission to cancel this appointment.')
            return redirect('dashboard:home')
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully.')
        return redirect('appointments:appointment_list')
    
    context = {
        'appointment': appointment,
        'user_profile': user_profile,
    }
    return render(request, 'appointments/cancel_appointment.html', context)


@login_required
def reschedule_appointment(request, pk):
    """Reschedule an appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check permissions
    if user_profile.user_type == 'patient':
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        if appointment.patient != patient_profile:
            messages.error(request, 'You do not have permission to reschedule this appointment.')
            return redirect('dashboard:home')
    
    if request.method == 'POST':
        new_date = request.POST.get('appointment_date')
        new_time = request.POST.get('appointment_time')
        
        # Check if the new time slot is available
        existing_appointment = Appointment.objects.filter(
            doctor=appointment.doctor,
            appointment_date=new_date,
            appointment_time=new_time,
            status__in=['scheduled', 'confirmed']
        ).exclude(id=appointment.id).exists()
        
        if existing_appointment:
            messages.error(request, 'This time slot is already booked. Please choose another time.')
        else:
            appointment.appointment_date = new_date
            appointment.appointment_time = new_time
            appointment.status = 'rescheduled'
            appointment.save()
            messages.success(request, 'Appointment rescheduled successfully.')
            return redirect('appointments:appointment_detail', pk=appointment.id)
    
    context = {
        'appointment': appointment,
        'user_profile': user_profile,
    }
    return render(request, 'appointments/reschedule_appointment.html', context)


@login_required
def update_appointment_status(request, pk):
    """Update appointment status (for doctors)"""
    appointment = get_object_or_404(Appointment, pk=pk)
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.user_type != 'doctor':
        messages.error(request, 'Only doctors can update appointment status.')
        return redirect('dashboard:home')
    
    doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
    if appointment.doctor != doctor_profile:
        messages.error(request, 'You do not have permission to update this appointment.')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        appointment.status = new_status
        if notes:
            appointment.notes = notes
        appointment.save()
        
        messages.success(request, 'Appointment status updated successfully.')
        return redirect('appointments:appointment_detail', pk=appointment.id)
    
    context = {
        'appointment': appointment,
        'user_profile': user_profile,
    }
    return render(request, 'appointments/update_status.html', context)

