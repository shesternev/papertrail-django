from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.manager = self.User.objects

    def test_create_user(self):
        email = 'testuser@example.com'
        phone_number = '1234567890'
        password = '1testpassword5gg1'

        user = self.manager.create_user(email=email, phone_number=phone_number, password=password)

        self.assertIsNotNone(user.pk)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_active)

        # Test that the email is normalized
        self.assertEqual(user.email, email.lower())

        # Test that the password is set and not plain text
        self.assertNotEqual(user.password, password)

        # Test that creating a user with the same email and phone number raises a ValidationError
        with self.assertRaises(IntegrityError):
            self.manager.create_user(email=email, phone_number=phone_number)

    def test_create_superuser(self):
        email = 'testadmin@example.com'
        phone_number = '1234567890'
        password = 'testpassword'

        user = self.manager.create_superuser(email=email, phone_number=phone_number, password=password)
        self.assertIsNotNone(user.pk)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        # Test that the email is normalized
        self.assertEqual(user.email, email.lower())

        # Test that the password is set and not plain text
        self.assertNotEqual(user.password, password)

        # Test that creating a superuser with the same email and phone number raises a ValidationError
        with self.assertRaises(IntegrityError):
            self.manager.create_superuser(email=email, phone_number=phone_number)
