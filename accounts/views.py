from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from .models import UserProfile, DoctorProfile, PatientProfile

# Create your views here.

def root_redirect(request):
    """Redirect root URL to dashboard for authenticated users with valid profiles, login otherwise"""
    if request.user.is_authenticated:
        # Check if user has a valid profile before redirecting to dashboard
        try:
            UserProfile.objects.get(user=request.user)
            return redirect('dashboard:home')
        except UserProfile.DoesNotExist:
            # No profile - check if admin/staff
            if request.user.is_superuser or request.user.is_staff:
                return redirect(reverse('admin:index'))
            # User is authenticated but has no profile - redirect to login
            # The login view will handle logging them out
            return redirect('accounts:login')
    return redirect('accounts:login')


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
        # Check if user has a valid profile before redirecting to dashboard
        try:
            UserProfile.objects.get(user=request.user)
            return redirect('dashboard:home')
        except UserProfile.DoesNotExist:
            # No profile - check if admin/staff
            if request.user.is_superuser or request.user.is_staff:
                return redirect(reverse('admin:index'))
            # User is authenticated but has no profile - log them out
            logout(request)
            messages.error(request, 'Your account profile could not be found. Please contact administrator.')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verify user has a profile before logging them in
            try:
                UserProfile.objects.get(user=user)
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('dashboard:home')
            except UserProfile.DoesNotExist:
                # No profile - check if admin/superuser
                if user.is_superuser or user.is_staff:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                    return redirect(reverse('admin:index'))
                messages.error(request, 'Your account profile could not be found. Please contact administrator.')
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

