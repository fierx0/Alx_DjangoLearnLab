from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User


class AuthFlowTests(APITestCase):
def test_register_then_login(self):
reg_url = reverse('register')
payload = {
'username': 'testuser',
'email': 'test@example.com',
'password': 'VeryStrong123',
'bio': 'hey there'
}
r = self.client.post(reg_url, payload, format='json')
self.assertEqual(r.status_code, status.HTTP_201_CREATED)
self.assertIn('token', r.data)


login_url = reverse('login')
r2 = self.client.post(login_url, {
'username': 'testuser', 'password': 'VeryStrong123'
}, format='json')
self.assertEqual(r2.status_code, status.HTTP_200_OK)
self.assertIn('token', r2.data)


def test_profile_requires_auth(self):
profile_url = reverse('profile')
r = self.client.get(profile_url)
self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


# login flow
User.objects.create_user(username='u1', password='P@ssw0rd123')
r2 = self.client.post(reverse('login'), {
'username': 'u1', 'password': 'P@ssw0rd123'
}, format='json')
token = r2.data['token']
self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
r3 = self.client.get(profile_url)
self.assertEqual(r3.status_code, status.HTTP_200_OK)