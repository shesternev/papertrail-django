from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory

from account.backends import EmailBackend, PhoneBackend

User = get_user_model()


class EmailBackendTestCase(TestCase):
    def setUp(self):
        self.backend = EmailBackend()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='test@example.com',
            phone_number=123456789,
            password='password'
        )

    def test_authenticate_with_valid_credentials(self):
        request = self.factory.post('/')
        user = self.backend.authenticate(request, email='test@example.com', password='password')
        self.assertEqual(user, self.user)

    def test_authenticate_with_invalid_email(self):
        request = self.factory.post('/')
        user = self.backend.authenticate(request, email='invalid@example.com', password='password')
        self.assertIsNone(user)

    def test_authenticate_with_invalid_password(self):
        request = self.factory.post('/')
        user = self.backend.authenticate(request, email='test@example.com', password='wrong_password')
        self.assertIsNone(user)

    def test_get_user_with_valid_user_id(self):
        user = self.backend.get_user(self.user.id)
        self.assertEqual(user, self.user)

    def test_get_user_with_invalid_user_id(self):
        user = self.backend.get_user(self.user.id + 1)
        self.assertIsNone(user)


class PhoneBackendTestCase(TestCase):

    def setUp(self):
        self.backend = PhoneBackend()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='test@email.com',
            phone_number='1234567890',
            password='password'
        )

    def test_authenticate_with_valid_credentials(self):
        request = self.factory.post('/')
        user = self.backend.authenticate(request, email='1234567890', password='password')
        self.assertEqual(user, self.user)

    def test_authenticate_with_invalid_phone_number(self):
        request = self.factory.post('/')
        user = self.backend.authenticate(request, email='9999999999', password='password')
        self.assertIsNone(user)

    def test_authenticate_with_invalid_password(self):
        request = self.factory.post('/')
        user = self.backend.authenticate(request, email='1234567890', password='wrong_password')
        self.assertIsNone(user)

    def test_get_user_with_valid_user_id(self):
        user = self.backend.get_user(self.user.id)
        self.assertEqual(user, self.user)

    def test_get_user_with_invalid_user_id(self):
        user = self.backend.get_user(self.user.id + 1)
        self.assertIsNone(user)
