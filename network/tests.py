from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, User

class NetworkTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            user=self.user,
            title='Initial Test Post',
            content='Test post content'
        )

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/login.html')

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/register.html')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('index'))

    def test_create_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('index'), {
            'title': 'Test Title',
            'content': 'New test post'
        })
        self.assertEqual(Post.objects.count(), 2)
        latest_post = Post.objects.latest('id')
        self.assertEqual(latest_post.content, 'New test post')
        self.assertEqual(latest_post.title, 'Test Title')

    def test_view_profile(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
