from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class AuthenticationTestCase(APITestCase):
    def test_user_registration(self):
        """Test user can register"""
        url = '/api/auth/register/'
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)

    def test_user_login(self):
        """Test user can login"""
        # Create user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Login
        url = '/api/auth/login/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
