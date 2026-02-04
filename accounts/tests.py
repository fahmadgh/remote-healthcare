from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import UserProfile, DoctorProfile, PatientProfile


class LoginRedirectTests(TestCase):
    """Test cases for login redirect behavior to prevent redirect loops"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        # Create a user with complete profile
        self.user_with_profile = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user_with_profile,
            user_type='patient',
            phone_number='1234567890'
        )
        self.patient_profile = PatientProfile.objects.create(
            user_profile=self.user_profile,
            blood_group='O+',
            emergency_contact='9876543210'
        )
        
        # Create a user without profile
        self.user_without_profile = User.objects.create_user(
            username='incompleteuser',
            email='incomplete@example.com',
            password='testpass123',
            first_name='Incomplete',
            last_name='User'
        )
    
    def test_login_with_valid_profile_redirects_to_dashboard(self):
        """Test that login with valid profile redirects to dashboard"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('dashboard:home'))
    
    def test_login_without_profile_shows_error(self):
        """Test that login without profile shows error message"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'incompleteuser',
            'password': 'testpass123'
        })
        # Should not redirect and should show error
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertTrue(any('profile could not be found' in str(m) for m in messages))
    
    def test_authenticated_user_with_profile_accessing_login_redirects_to_dashboard(self):
        """Test that authenticated user accessing login page redirects to dashboard"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:login'))
        self.assertRedirects(response, reverse('dashboard:home'))
    
    def test_authenticated_user_without_profile_gets_logged_out(self):
        """Test that authenticated user without profile is logged out from login page"""
        # Force login the user without profile
        self.client.force_login(self.user_without_profile)
        response = self.client.get(reverse('accounts:login'))
        # Should show login page with error message
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertTrue(any('profile could not be found' in str(m) for m in messages))
        # User should be logged out
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_root_url_redirects_unauthenticated_to_login(self):
        """Test that root URL redirects unauthenticated users to login"""
        response = self.client.get('/')
        self.assertRedirects(response, reverse('accounts:login'))
    
    def test_root_url_redirects_authenticated_to_dashboard(self):
        """Test that root URL redirects authenticated users to dashboard"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/')
        self.assertRedirects(response, reverse('dashboard:home'))
    
    def test_root_url_with_authenticated_user_without_profile_redirects_to_login(self):
        """Test that root URL redirects authenticated users without profile to login"""
        # Force login the user without profile
        self.client.force_login(self.user_without_profile)
        response = self.client.get('/')
        self.assertRedirects(response, reverse('accounts:login'))
