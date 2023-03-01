from djoser.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth import get_user_model

from account.serializers import TokenSerializer, UserCreateSerializer

User = get_user_model()


class TokenSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            phone_number='1234567890',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        self.token = settings.TOKEN_MODEL.objects.create(user=self.user)
        self.serializer = TokenSerializer(instance=self.token)
        self.client = APIClient()

    def test_token_serializer_returns_token(self):
        data = self.serializer.data
        self.assertIn('auth_token', data)
        self.assertIn('user', data)
        self.assertEqual(data['user'], self.user.pk)


class UserCreateSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.validated_data = {
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
        }

    def test_user_create_serializer_creates_user(self):
        serializer = UserCreateSerializer(data=self.validated_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.assertEqual(user.email, self.validated_data['email'])
        self.assertEqual(user.phone_number, self.validated_data['phone_number'])
        self.assertTrue(user.check_password(self.validated_data['password']))
        self.assertEqual(user.first_name, self.validated_data['first_name'])
        self.assertEqual(user.last_name, self.validated_data['last_name'])

    def test_user_create_serializer_validates_email(self):
        self.validated_data['email'] = 'invalid-email'
        serializer = UserCreateSerializer(data=self.validated_data)
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        self.assertIn('email', cm.exception.detail)
        self.assertEqual(cm.exception.detail['email'][0].code, 'invalid')
