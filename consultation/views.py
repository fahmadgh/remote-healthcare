from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.models import UserProfile, DoctorProfile, PatientProfile
from appointments.models import Appointment
from .models import ConsultationNote, ChatMessage, VideoSession
import uuid

# Create your views here.

@login_required
def consultation_notes_list(request):
    """List consultation notes"""
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.user_type == 'doctor':
        doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
        notes = ConsultationNote.objects.filter(doctor=doctor_profile)
    else:
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        notes = ConsultationNote.objects.filter(patient=patient_profile)
    
    context = {
        'notes': notes,
        'user_profile': user_profile,
    }
    return render(request, 'consultation/notes_list.html', context)


@login_required
def create_consultation_note(request, appointment_id):
    """Create consultation note for an appointment (for doctors)"""
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.user_type != 'doctor':
        messages.error(request, 'Only doctors can create consultation notes.')
        return redirect('dashboard:home')
    
    doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    if appointment.doctor != doctor_profile:
        messages.error(request, 'You do not have permission to create notes for this appointment.')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        chief_complaint = request.POST.get('chief_complaint')
        history = request.POST.get('history', '')
        examination = request.POST.get('examination', '')
        diagnosis = request.POST.get('diagnosis')
        treatment_plan = request.POST.get('treatment_plan')
        follow_up = request.POST.get('follow_up', '')
        
        note = ConsultationNote.objects.create(
            appointment=appointment,
            doctor=doctor_profile,
            patient=appointment.patient,
            chief_complaint=chief_complaint,
            history=history,
            examination=examination,
            diagnosis=diagnosis,
            treatment_plan=treatment_plan,
            follow_up=follow_up
        )
        
        # Update appointment status to completed
        appointment.status = 'completed'
        appointment.save()
        
        messages.success(request, 'Consultation note created successfully.')
        return redirect('consultation:note_detail', pk=note.id)
    
    context = {
        'appointment': appointment,
        'user_profile': user_profile,
    }
    return render(request, 'consultation/create_note.html', context)


@login_required
def consultation_note_detail(request, pk):
    """View consultation note details"""
    note = get_object_or_404(ConsultationNote, pk=pk)
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check permissions
    if user_profile.user_type == 'patient':
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        if note.patient != patient_profile:
            messages.error(request, 'You do not have permission to view this note.')
            return redirect('dashboard:home')
    
    context = {
        'note': note,
        'user_profile': user_profile,
    }
    return render(request, 'consultation/note_detail.html', context)


@login_required
def chat_interface(request, appointment_id):
    """Chat interface for an appointment"""
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check permissions
    if user_profile.user_type == 'doctor':
        doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
        if appointment.doctor != doctor_profile:
            messages.error(request, 'You do not have permission to access this chat.')
            return redirect('dashboard:home')
    else:
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        if appointment.patient != patient_profile:
            messages.error(request, 'You do not have permission to access this chat.')
            return redirect('dashboard:home')
    
    # Get chat messages
    messages_list = ChatMessage.objects.filter(appointment=appointment)
    
    # Mark messages as read
    ChatMessage.objects.filter(appointment=appointment).exclude(sender=request.user).update(is_read=True)
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            ChatMessage.objects.create(
                appointment=appointment,
                sender=request.user,
                message=message_text
            )
            return redirect('consultation:chat', appointment_id=appointment_id)
    
    context = {
        'appointment': appointment,
        'messages_list': messages_list,
        'user_profile': user_profile,
    }
    return render(request, 'consultation/chat.html', context)


@login_required
def video_session(request, appointment_id):
    """Video consultation interface"""
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check permissions
    if user_profile.user_type == 'doctor':
        doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
        if appointment.doctor != doctor_profile:
            messages.error(request, 'You do not have permission to access this video session.')
            return redirect('dashboard:home')
    else:
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        if appointment.patient != patient_profile:
            messages.error(request, 'You do not have permission to access this video session.')
            return redirect('dashboard:home')
    
    # Get or create video session
    video_session, created = VideoSession.objects.get_or_create(
        appointment=appointment,
        defaults={'session_id': str(uuid.uuid4())}
    )
    
    context = {
        'appointment': appointment,
        'video_session': video_session,
        'user_profile': user_profile,
    }
    return render(request, 'consultation/video_session.html', context)


@login_required
def start_video_session(request, appointment_id):
    """Start a video session"""
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    try:
        video_session = VideoSession.objects.get(appointment=appointment)
        video_session.status = 'active'
        video_session.start_time = timezone.now()
        video_session.save()
        messages.success(request, 'Video session started.')
    except VideoSession.DoesNotExist:
        messages.error(request, 'Video session not found.')
    
    return redirect('consultation:video_session', appointment_id=appointment_id)


@login_required
def end_video_session(request, appointment_id):
    """End a video session"""
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    try:
        video_session = VideoSession.objects.get(appointment=appointment)
        video_session.status = 'completed'
        video_session.end_time = timezone.now()
        
        if video_session.start_time:
            duration = (video_session.end_time - video_session.start_time).total_seconds() / 60
            video_session.duration_minutes = int(duration)
        
        video_session.save()
        messages.success(request, 'Video session ended.')
    except VideoSession.DoesNotExist:
        messages.error(request, 'Video session not found.')
    
    return redirect('appointments:appointment_detail', pk=appointment_id)

