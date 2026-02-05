#!/usr/bin/env python
"""
Script to populate the database with sample data for testing
"""
import os
import sys
import django
from datetime import datetime, timedelta, time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_system.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile, DoctorProfile, PatientProfile
from appointments.models import Appointment, DoctorAvailability
from reports.models import MedicalRecord, Report
from consultation.models import ConsultationNote

def create_sample_data():
    print("Creating sample data...")
    
    # Create Admin User
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✓ Created admin user: admin / admin123")
    else:
        # Update existing admin user to ensure proper flags and password
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✓ Admin user already exists: admin (updated)")
    
    # Create Doctor User
    doctor_user, created = User.objects.get_or_create(
        username='drsmith',
        defaults={
            'email': 'drsmith@example.com',
            'first_name': 'John',
            'last_name': 'Smith'
        }
    )
    if created:
        doctor_user.set_password('doctor123')
        doctor_user.save()
        print(f"✓ Created doctor user: drsmith / doctor123")
    
    # Create Doctor Profile
    doctor_profile, created = UserProfile.objects.get_or_create(
        user=doctor_user,
        defaults={
            'user_type': 'doctor',
            'phone_number': '+1234567890',
            'address': '123 Medical Center, Healthcare City'
        }
    )
    
    # Create Doctor Info
    doctor_info, created = DoctorProfile.objects.get_or_create(
        user_profile=doctor_profile,
        defaults={
            'specialization': 'General Physician',
            'qualification': 'MD, MBBS',
            'license_number': 'DOC12345',
            'experience_years': 10,
            'consultation_fee': 100.00,
            'available': True,
            'bio': 'Experienced general physician with 10 years of practice.'
        }
    )
    if created:
        print(f"✓ Created doctor profile for Dr. {doctor_user.get_full_name()}")
    
    # Create Doctor Availability
    for day in range(1, 6):  # Monday to Friday
        DoctorAvailability.objects.get_or_create(
            doctor=doctor_info,
            day_of_week=day,
            start_time=time(9, 0),
            defaults={
                'end_time': time(17, 0),
                'is_available': True
            }
        )
    
    # Create another Doctor
    doctor2_user, created = User.objects.get_or_create(
        username='drjohnson',
        defaults={
            'email': 'drjohnson@example.com',
            'first_name': 'Emily',
            'last_name': 'Johnson'
        }
    )
    if created:
        doctor2_user.set_password('doctor123')
        doctor2_user.save()
        print(f"✓ Created doctor user: drjohnson / doctor123")
    
    doctor2_profile, created = UserProfile.objects.get_or_create(
        user=doctor2_user,
        defaults={
            'user_type': 'doctor',
            'phone_number': '+1234567891'
        }
    )
    
    doctor2_info, created = DoctorProfile.objects.get_or_create(
        user_profile=doctor2_profile,
        defaults={
            'specialization': 'Cardiologist',
            'qualification': 'MD, DM Cardiology',
            'license_number': 'DOC67890',
            'experience_years': 15,
            'consultation_fee': 150.00,
            'available': True
        }
    )
    
    # Create Patient User
    patient_user, created = User.objects.get_or_create(
        username='patient1',
        defaults={
            'email': 'patient1@example.com',
            'first_name': 'Alice',
            'last_name': 'Brown'
        }
    )
    if created:
        patient_user.set_password('patient123')
        patient_user.save()
        print(f"✓ Created patient user: patient1 / patient123")
    
    # Create Patient Profile
    patient_profile, created = UserProfile.objects.get_or_create(
        user=patient_user,
        defaults={
            'user_type': 'patient',
            'phone_number': '+1987654321',
            'address': '456 Residential Area, City'
        }
    )
    
    # Create Patient Info
    patient_info, created = PatientProfile.objects.get_or_create(
        user_profile=patient_profile,
        defaults={
            'blood_group': 'A+',
            'emergency_contact': '+1987654322',
            'emergency_contact_name': 'Bob Brown',
            'allergies': 'Penicillin',
            'chronic_conditions': 'None'
        }
    )
    if created:
        print(f"✓ Created patient profile for {patient_user.get_full_name()}")
    
    # Create another Patient
    patient2_user, created = User.objects.get_or_create(
        username='patient2',
        defaults={
            'email': 'patient2@example.com',
            'first_name': 'Charlie',
            'last_name': 'Davis'
        }
    )
    if created:
        patient2_user.set_password('patient123')
        patient2_user.save()
        print(f"✓ Created patient user: patient2 / patient123")
    
    patient2_profile, created = UserProfile.objects.get_or_create(
        user=patient2_user,
        defaults={
            'user_type': 'patient',
            'phone_number': '+1987654323'
        }
    )
    
    patient2_info, created = PatientProfile.objects.get_or_create(
        user_profile=patient2_profile,
        defaults={
            'blood_group': 'O+',
            'emergency_contact': '+1987654324',
            'emergency_contact_name': 'Diana Davis'
        }
    )
    
    # Create Appointments
    today = datetime.now().date()
    
    # Past appointment
    apt1, created = Appointment.objects.get_or_create(
        patient=patient_info,
        doctor=doctor_info,
        appointment_date=today - timedelta(days=7),
        appointment_time=time(10, 0),
        defaults={
            'status': 'completed',
            'reason': 'Regular checkup and flu symptoms',
            'notes': 'Patient recovered well'
        }
    )
    if created:
        print(f"✓ Created past appointment")
    
    # Upcoming appointment
    apt2, created = Appointment.objects.get_or_create(
        patient=patient_info,
        doctor=doctor_info,
        appointment_date=today + timedelta(days=3),
        appointment_time=time(14, 0),
        defaults={
            'status': 'confirmed',
            'reason': 'Follow-up consultation',
        }
    )
    if created:
        print(f"✓ Created upcoming appointment")
    
    # Another upcoming appointment
    apt3, created = Appointment.objects.get_or_create(
        patient=patient2_info,
        doctor=doctor2_info,
        appointment_date=today + timedelta(days=5),
        appointment_time=time(11, 0),
        defaults={
            'status': 'scheduled',
            'reason': 'Heart checkup',
        }
    )
    
    # Create Medical Record
    record, created = MedicalRecord.objects.get_or_create(
        patient=patient_info,
        doctor=doctor_info,
        appointment=apt1,
        defaults={
            'diagnosis': 'Common cold with mild fever',
            'symptoms': 'Cough, runny nose, mild fever (100°F)',
            'prescription': 'Paracetamol 500mg - 3 times daily for 3 days\nRest and plenty of fluids',
            'lab_results': 'No lab tests required',
            'notes': 'Patient advised to return if symptoms persist after 3 days'
        }
    )
    if created:
        print(f"✓ Created medical record")
    
    # Create Consultation Note
    note, created = ConsultationNote.objects.get_or_create(
        appointment=apt1,
        doctor=doctor_info,
        patient=patient_info,
        defaults={
            'chief_complaint': 'Flu-like symptoms for 2 days',
            'history': 'No prior medical history. No allergies except Penicillin.',
            'examination': 'Temperature: 100°F, BP: 120/80, Throat: Slightly red',
            'diagnosis': 'Viral upper respiratory tract infection',
            'treatment_plan': 'Symptomatic treatment with antipyretics and rest',
            'follow_up': 'Follow up if symptoms worsen or persist beyond 5 days'
        }
    )
    if created:
        print(f"✓ Created consultation note")
    
    # Create Report
    report, created = Report.objects.get_or_create(
        patient=patient_info,
        doctor=doctor_info,
        medical_record=record,
        defaults={
            'report_type': 'consultation',
            'title': 'Consultation Summary - Common Cold',
            'content': '''Patient: Alice Brown
Date: {}
Doctor: Dr. John Smith

Chief Complaint: Flu-like symptoms
Diagnosis: Viral upper respiratory tract infection

Treatment:
- Paracetamol 500mg TDS for 3 days
- Rest and hydration

Follow-up: As needed if symptoms persist'''.format((today - timedelta(days=7)).strftime('%Y-%m-%d'))
        }
    )
    if created:
        print(f"✓ Created consultation report")
    
    print("\n" + "="*50)
    print("Sample data created successfully!")
    print("="*50)
    print("\nLogin credentials:")
    print("-" * 50)
    print("Admin:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nDoctor 1:")
    print("  Username: drsmith")
    print("  Password: doctor123")
    print("\nDoctor 2:")
    print("  Username: drjohnson")
    print("  Password: doctor123")
    print("\nPatient 1:")
    print("  Username: patient1")
    print("  Password: patient123")
    print("\nPatient 2:")
    print("  Username: patient2")
    print("  Password: patient123")
    print("-" * 50)

if __name__ == '__main__':
    create_sample_data()
