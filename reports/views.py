from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from accounts.models import UserProfile, DoctorProfile, PatientProfile
from .models import MedicalRecord, Report
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import csv
from io import BytesIO

# Create your views here.

@login_required
def medical_records_list(request):
    """List medical records"""
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.user_type == 'doctor':
        doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
        medical_records = MedicalRecord.objects.filter(doctor=doctor_profile)
    else:
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        medical_records = MedicalRecord.objects.filter(patient=patient_profile)
    
    context = {
        'medical_records': medical_records,
        'user_profile': user_profile,
    }
    return render(request, 'reports/medical_records_list.html', context)


@login_required
def medical_record_detail(request, pk):
    """View medical record details"""
    medical_record = get_object_or_404(MedicalRecord, pk=pk)
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check permissions
    if user_profile.user_type == 'doctor':
        doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
        # Doctors can view records they created
    else:
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        if medical_record.patient != patient_profile:
            messages.error(request, 'You do not have permission to view this record.')
            return redirect('dashboard:home')
    
    context = {
        'medical_record': medical_record,
        'user_profile': user_profile,
    }
    return render(request, 'reports/medical_record_detail.html', context)


@login_required
def create_medical_record(request):
    """Create a new medical record (for doctors)"""
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.user_type != 'doctor':
        messages.error(request, 'Only doctors can create medical records.')
        return redirect('dashboard:home')
    
    doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        diagnosis = request.POST.get('diagnosis')
        symptoms = request.POST.get('symptoms')
        prescription = request.POST.get('prescription')
        lab_results = request.POST.get('lab_results', '')
        notes = request.POST.get('notes', '')
        
        patient = get_object_or_404(PatientProfile, id=patient_id)
        
        medical_record = MedicalRecord.objects.create(
            patient=patient,
            doctor=doctor_profile,
            diagnosis=diagnosis,
            symptoms=symptoms,
            prescription=prescription,
            lab_results=lab_results,
            notes=notes
        )
        
        messages.success(request, 'Medical record created successfully.')
        return redirect('reports:medical_record_detail', pk=medical_record.id)
    
    # Get list of patients
    patients = PatientProfile.objects.all()
    
    context = {
        'patients': patients,
        'user_profile': user_profile,
    }
    return render(request, 'reports/create_medical_record.html', context)


@login_required
def reports_list(request):
    """List all reports"""
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.user_type == 'doctor':
        doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
        reports = Report.objects.filter(doctor=doctor_profile)
    else:
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        reports = Report.objects.filter(patient=patient_profile)
    
    context = {
        'reports': reports,
        'user_profile': user_profile,
    }
    return render(request, 'reports/reports_list.html', context)


@login_required
def generate_report(request):
    """Generate a new report (for doctors)"""
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.user_type != 'doctor':
        messages.error(request, 'Only doctors can generate reports.')
        return redirect('dashboard:home')
    
    doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        report_type = request.POST.get('report_type')
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        patient = get_object_or_404(PatientProfile, id=patient_id)
        
        report = Report.objects.create(
            patient=patient,
            doctor=doctor_profile,
            report_type=report_type,
            title=title,
            content=content
        )
        
        messages.success(request, 'Report generated successfully.')
        return redirect('reports:report_detail', pk=report.id)
    
    # Get list of patients
    patients = PatientProfile.objects.all()
    
    context = {
        'patients': patients,
        'user_profile': user_profile,
    }
    return render(request, 'reports/generate_report.html', context)


@login_required
def report_detail(request, pk):
    """View report details"""
    report = get_object_or_404(Report, pk=pk)
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check permissions
    if user_profile.user_type == 'patient':
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        if report.patient != patient_profile:
            messages.error(request, 'You do not have permission to view this report.')
            return redirect('dashboard:home')
    
    context = {
        'report': report,
        'user_profile': user_profile,
    }
    return render(request, 'reports/report_detail.html', context)


@login_required
def export_report_pdf(request, pk):
    """Export report as PDF"""
    report = get_object_or_404(Report, pk=pk)
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check permissions
    if user_profile.user_type == 'patient':
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        if report.patient != patient_profile:
            messages.error(request, 'You do not have permission to access this report.')
            return redirect('dashboard:home')
    
    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add content to PDF
    p.setFont("Helvetica-Bold", 16)
    p.drawString(1 * inch, 10 * inch, "Healthcare System Report")
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(1 * inch, 9.5 * inch, f"Title: {report.title}")
    
    p.setFont("Helvetica", 10)
    p.drawString(1 * inch, 9.2 * inch, f"Patient: {report.patient.user_profile.user.get_full_name()}")
    p.drawString(1 * inch, 9 * inch, f"Doctor: Dr. {report.doctor.user_profile.user.get_full_name()}")
    p.drawString(1 * inch, 8.8 * inch, f"Date: {report.created_at.strftime('%Y-%m-%d')}")
    p.drawString(1 * inch, 8.6 * inch, f"Type: {report.get_report_type_display()}")
    
    # Add report content
    p.setFont("Helvetica-Bold", 11)
    p.drawString(1 * inch, 8.2 * inch, "Report Content:")
    
    p.setFont("Helvetica", 10)
    # Split content into lines
    text = p.beginText(1 * inch, 7.9 * inch)
    for line in report.content.split('\n'):
        text.textLine(line[:90])  # Limit line length
    p.drawText(text)
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{report.id}.pdf"'
    
    return response


@login_required
def export_report_csv(request, pk):
    """Export report as CSV"""
    report = get_object_or_404(Report, pk=pk)
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check permissions
    if user_profile.user_type == 'patient':
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        if report.patient != patient_profile:
            messages.error(request, 'You do not have permission to access this report.')
            return redirect('dashboard:home')
    
    # Create CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="report_{report.id}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Field', 'Value'])
    writer.writerow(['Title', report.title])
    writer.writerow(['Patient', report.patient.user_profile.user.get_full_name()])
    writer.writerow(['Doctor', f"Dr. {report.doctor.user_profile.user.get_full_name()}"])
    writer.writerow(['Date', report.created_at.strftime('%Y-%m-%d')])
    writer.writerow(['Type', report.get_report_type_display()])
    writer.writerow(['Content', report.content])
    
    return response

