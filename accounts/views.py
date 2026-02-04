from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, DoctorProfile, PatientProfile

# Create your views here.

def register(request):
    """User registration view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_type = request.POST.get('user_type')
        phone_number = request.POST.get('phone_number', '')
        
        # Validation
        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'accounts/register.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create user profile
        user_profile = UserProfile.objects.create(
            user=user,
            user_type=user_type,
            phone_number=phone_number
        )
        
        # Create specific profile based on user type
        if user_type == 'doctor':
            specialization = request.POST.get('specialization', '')
            qualification = request.POST.get('qualification', '')
            license_number = request.POST.get('license_number', '')
            DoctorProfile.objects.create(
                user_profile=user_profile,
                specialization=specialization,
                qualification=qualification,
                license_number=license_number
            )
        else:
            blood_group = request.POST.get('blood_group', '')
            emergency_contact = request.POST.get('emergency_contact', '')
            PatientProfile.objects.create(
                user_profile=user_profile,
                blood_group=blood_group,
                emergency_contact=emergency_contact
            )
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('accounts:login')
    
    return render(request, 'accounts/register.html')


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def profile(request):
    """User profile view"""
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.user_type == 'doctor':
        doctor_profile = DoctorProfile.objects.get(user_profile=user_profile)
        context = {
            'user_profile': user_profile,
            'doctor_profile': doctor_profile,
        }
    else:
        patient_profile = PatientProfile.objects.get(user_profile=user_profile)
        context = {
            'user_profile': user_profile,
            'patient_profile': patient_profile,
        }
    
    return render(request, 'accounts/profile.html', context)

