#!/usr/bin/env python
"""
Test cases for populate_db.py script
"""
import os
import sys
import django
from django.test import TestCase

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_system.settings')
django.setup()

from django.contrib.auth.models import User


class PopulateDBAdminTests(TestCase):
    """Test cases for admin user creation in populate_db.py"""
    
    def test_admin_user_creation(self):
        """Test that populate_db creates an admin user with correct properties"""
        # Import and run the populate script
        from populate_db import create_sample_data
        create_sample_data()
        
        # Verify admin user exists
        admin = User.objects.get(username='admin')
        
        # Verify admin properties
        self.assertEqual(admin.username, 'admin')
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertEqual(admin.first_name, 'Admin')
        self.assertEqual(admin.last_name, 'User')
        self.assertTrue(admin.is_staff, "Admin user should have is_staff=True")
        self.assertTrue(admin.is_superuser, "Admin user should have is_superuser=True")
        self.assertTrue(admin.check_password('admin123'), "Admin password should be 'admin123'")
    
    def test_admin_user_idempotency(self):
        """Test that running populate_db multiple times doesn't create duplicate admins"""
        from populate_db import create_sample_data
        
        # Run populate_db twice
        create_sample_data()
        create_sample_data()
        
        # Verify only one admin user exists
        admin_count = User.objects.filter(username='admin').count()
        self.assertEqual(admin_count, 1, "Should have exactly one admin user")
        
        # Verify admin still has correct properties
        admin = User.objects.get(username='admin')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', 'test_populate_db'])
