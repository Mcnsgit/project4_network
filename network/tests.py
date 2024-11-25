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
            title='Test Title',
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
        # First login
        login = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login)  # Verify login was successful
        
        # Attempt to create post
        response = self.client.post(reverse('index'), {
            'title': 'Test Title',
            'content': 'New test post'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful post
        self.assertEqual(Post.objects.count(), 2)  # One from setUp + one new
        
        # Verify the new post
        latest_post = Post.objects.latest('created_at')
        self.assertEqual(latest_post.title, 'Test Title')
        self.assertEqual(latest_post.content, 'New test post')
        self.assertEqual(latest_post.user, self.user)

    def test_view_profile(self):
        # First login
        login = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login)

        # Try to access profile
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, 'Test Title')  # Check for post title
