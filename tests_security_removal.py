"""
Test to verify CSRF protection has been removed
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class CSRFDisabledTest(TestCase):
    """Test that CSRF protection has been disabled"""
    
    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_login_without_csrf_token(self):
        """Test that login form works without CSRF token"""
        # Note: enforce_csrf_checks parameter has no effect when CSRF middleware
        # is disabled globally. This test verifies that POST requests succeed
        # without CSRF tokens, which would normally fail with a 403 error.
        response = self.client.post(
            reverse('accounts:login'),
            {
                'username': 'testuser',
                'password': 'testpass123'
            },
            enforce_csrf_checks=True  # Would normally enforce CSRF, but middleware is disabled
        )
        # Should redirect or succeed without CSRF error
        # A 403 Forbidden would indicate CSRF protection is still active
        self.assertNotEqual(response.status_code, 403,
                          "CSRF protection appears to still be active!")
        print(f"✓ Login form accepts POST without CSRF token (status: {response.status_code})")
    
    def test_csrf_middleware_disabled(self):
        """Verify CSRF middleware is not in settings"""
        from django.conf import settings
        csrf_middleware = 'django.middleware.csrf.CsrfViewMiddleware'
        self.assertNotIn(csrf_middleware, settings.MIDDLEWARE,
                        "CSRF middleware should be removed from settings")
        print("✓ CSRF middleware is not in MIDDLEWARE list")
    
    def test_login_template_no_csrf_token(self):
        """Verify login template doesn't contain csrf_token"""
        response = self.client.get(reverse('accounts:login'))
        content = response.content.decode()
        self.assertNotIn('{% csrf_token %}', content,
                        "Login template should not contain csrf_token tag")
        self.assertNotIn('csrfmiddlewaretoken', content,
                        "Login form should not contain CSRF token field")
        print("✓ Login template does not contain CSRF token")


class PlaintextDataStorageTest(TestCase):
    """Test that medical data is stored in plaintext"""
    
    def test_medical_record_model_fields_are_plaintext(self):
        """Verify MedicalRecord model uses TextField (no encryption)"""
        from reports.models import MedicalRecord
        from django.db import models
        
        # Check that sensitive fields are TextField (not encrypted)
        diagnosis_field = MedicalRecord._meta.get_field('diagnosis')
        symptoms_field = MedicalRecord._meta.get_field('symptoms')
        prescription_field = MedicalRecord._meta.get_field('prescription')
        lab_results_field = MedicalRecord._meta.get_field('lab_results')
        
        self.assertIsInstance(diagnosis_field, models.TextField,
                            "Diagnosis should be plaintext TextField")
        self.assertIsInstance(symptoms_field, models.TextField,
                            "Symptoms should be plaintext TextField")
        self.assertIsInstance(prescription_field, models.TextField,
                            "Prescription should be plaintext TextField")
        self.assertIsInstance(lab_results_field, models.TextField,
                            "Lab results should be plaintext TextField")
        
        print("✓ Medical record fields are plaintext TextField (no encryption)")
    
    def test_patient_profile_sensitive_fields_plaintext(self):
        """Verify PatientProfile sensitive fields are plaintext"""
        from accounts.models import PatientProfile
        from django.db import models
        
        blood_group_field = PatientProfile._meta.get_field('blood_group')
        allergies_field = PatientProfile._meta.get_field('allergies')
        chronic_conditions_field = PatientProfile._meta.get_field('chronic_conditions')
        
        self.assertIsInstance(blood_group_field, models.CharField,
                            "Blood group should be plaintext CharField")
        self.assertIsInstance(allergies_field, models.TextField,
                            "Allergies should be plaintext TextField")
        self.assertIsInstance(chronic_conditions_field, models.TextField,
                            "Chronic conditions should be plaintext TextField")
        
        print("✓ Patient profile sensitive fields are plaintext (no encryption)")
