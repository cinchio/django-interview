from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_post(self):
        """Test creating a blog post"""
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertIsNotNone(post.slug)


class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            published=True
        )

    def test_list_posts(self):
        """Test listing blog posts"""
        url = '/api/posts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_authenticated(self):
        """Test authenticated user can create post"""
        self.client.force_authenticate(user=self.user)
        url = '/api/posts/'
        data = {
            'title': 'New Post',
            'content': 'New content'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_unauthenticated(self):
        """Test unauthenticated user cannot create post"""
        url = '/api/posts/'
        data = {
            'title': 'New Post',
            'content': 'New content'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
