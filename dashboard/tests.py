from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import UserProfile, DoctorProfile, PatientProfile


class DashboardRedirectTests(TestCase):
    """Test cases for dashboard redirect behavior to prevent redirect loops"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        # Create a user with complete patient profile
        self.patient_user = User.objects.create_user(
            username='patientuser',
            email='patient@example.com',
            password='testpass123',
            first_name='Patient',
            last_name='User'
        )
        self.patient_user_profile = UserProfile.objects.create(
            user=self.patient_user,
            user_type='patient',
            phone_number='1234567890'
        )
        self.patient_profile = PatientProfile.objects.create(
            user_profile=self.patient_user_profile,
            blood_group='O+',
            emergency_contact='9876543210'
        )
        
        # Create a user with complete doctor profile
        self.doctor_user = User.objects.create_user(
            username='doctoruser',
            email='doctor@example.com',
            password='testpass123',
            first_name='Doctor',
            last_name='User'
        )
        self.doctor_user_profile = UserProfile.objects.create(
            user=self.doctor_user,
            user_type='doctor',
            phone_number='1234567890'
        )
        self.doctor_profile = DoctorProfile.objects.create(
            user_profile=self.doctor_user_profile,
            specialization='Cardiology',
            qualification='MD',
            license_number='DOC123'
        )
        
        # Create a user without profile
        self.user_without_profile = User.objects.create_user(
            username='incompleteuser',
            email='incomplete@example.com',
            password='testpass123',
            first_name='Incomplete',
            last_name='User'
        )
    
    def test_dashboard_home_with_patient_profile_renders_correctly(self):
        """Test that dashboard home with patient profile works correctly"""
        self.client.login(username='patientuser', password='testpass123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/patient_dashboard.html')
    
    def test_dashboard_home_with_doctor_profile_renders_correctly(self):
        """Test that dashboard home with doctor profile works correctly"""
        self.client.login(username='doctoruser', password='testpass123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/doctor_dashboard.html')
    
    def test_dashboard_home_without_profile_logs_out_user(self):
        """Test that dashboard home without profile logs out user and redirects"""
        # Force login the user without profile
        self.client.force_login(self.user_without_profile)
        response = self.client.get(reverse('dashboard:home'), follow=True)
        # Should redirect to login
        self.assertEqual(response.redirect_chain[-1][0], reverse('accounts:login'))
        # Check that user was logged out
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        # Check for error message
        messages = list(response.context['messages'])
        self.assertTrue(any('profile not found' in str(m).lower() for m in messages))
    
    def test_unauthenticated_user_redirected_to_login(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
