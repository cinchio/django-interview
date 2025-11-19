from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Page


class PageModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_page(self):
        """Test creating a page"""
        page = Page.objects.create(
            title='About Us',
            content='About our company',
            author=self.user
        )
        self.assertEqual(page.title, 'About Us')
        self.assertEqual(page.author, self.user)
        self.assertIsNotNone(page.slug)


class PageAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.page = Page.objects.create(
            title='About Us',
            content='About our company',
            author=self.user,
            published=True
        )

    def test_list_pages(self):
        """Test listing pages"""
        url = '/api/pages/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_page_by_slug(self):
        """Test getting page by slug"""
        url = f'/api/pages/{self.page.slug}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_page_authenticated(self):
        """Test authenticated user can create page"""
        self.client.force_authenticate(user=self.user)
        url = '/api/pages/'
        data = {
            'title': 'Contact',
            'content': 'Contact us'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_page_unauthenticated(self):
        """Test unauthenticated user cannot create page"""
        url = '/api/pages/'
        data = {
            'title': 'Contact',
            'content': 'Contact us'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
