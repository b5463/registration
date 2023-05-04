from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class Tests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')

    def test_registerPage_GET(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_registerPage_POST(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newtestpass',
            'password2': 'newtestpass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_loginPage_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_loginPage_POST(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_logoutUser_GET(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_home_GET(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')