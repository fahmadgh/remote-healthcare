from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import UserProfile
from .models import UserSettings, SystemSettings

# Create your views here.

@login_required
def user_settings(request):
    """User settings page"""
    user_profile = UserProfile.objects.get(user=request.user)
    user_settings_obj, created = UserSettings.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update personal details
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        
        # Update profile
        user_profile.phone_number = request.POST.get('phone_number', '')
        user_profile.address = request.POST.get('address', '')
        user_profile.email_notifications = request.POST.get('email_notifications') == 'on'
        user_profile.sms_notifications = request.POST.get('sms_notifications') == 'on'
        user_profile.save()
        
        # Update user settings
        user_settings_obj.profile_visibility = request.POST.get('profile_visibility') == 'on'
        user_settings_obj.show_phone = request.POST.get('show_phone') == 'on'
        user_settings_obj.show_email = request.POST.get('show_email') == 'on'
        user_settings_obj.theme = request.POST.get('theme', 'light')
        user_settings_obj.allow_messages = request.POST.get('allow_messages') == 'on'
        user_settings_obj.allow_video_calls = request.POST.get('allow_video_calls') == 'on'
        user_settings_obj.save()
        
        messages.success(request, 'Settings updated successfully.')
        return redirect('settings_app:user_settings')
    
    context = {
        'user_profile': user_profile,
        'user_settings': user_settings_obj,
    }
    return render(request, 'settings_app/user_settings.html', context)


@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings_app:user_settings')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'settings_app/change_password.html', context)


@login_required
def system_settings(request):
    """System settings page (admin only)"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access system settings.')
        return redirect('dashboard:home')
    
    settings = SystemSettings.objects.all()
    
    if request.method == 'POST':
        # Update system settings
        for setting in settings:
            new_value = request.POST.get(f'setting_{setting.id}')
            if new_value is not None:
                setting.setting_value = new_value
                setting.save()
        
        messages.success(request, 'System settings updated successfully.')
        return redirect('settings_app:system_settings')
    
    context = {
        'settings': settings,
    }
    return render(request, 'settings_app/system_settings.html', context)

