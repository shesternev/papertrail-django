from django.test import TestCase
from django.contrib.auth import get_user_model

from account.forms import CustomUserCreationForm


class CustomUserCreationFormTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'phone_number': '123456789',
            'password1': 'fgqrg15hatw',
            'password2': 'fgqrg15hatw',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_valid_form(self):
        form = CustomUserCreationForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_missing_first_name(self):
        self.user_data['first_name'] = ''
        form = CustomUserCreationForm(data=self.user_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'], ['This field is required.'])

    def test_missing_last_name(self):
        self.user_data['last_name'] = ''
        form = CustomUserCreationForm(data=self.user_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['last_name'], ['This field is required.'])

    def test_email_already_exists(self):
        get_user_model().objects.create_user(
            email=self.user_data['email'],
            phone_number='123456789',
            password=self.user_data['password1']
        )
        form = CustomUserCreationForm(data=self.user_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['User with this Email address already exists.'])

    def test_passwords_do_not_match(self):
        self.user_data['password2'] = 'differentpassword'
        form = CustomUserCreationForm(data=self.user_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])

    def test_password_too_short(self):
        self.user_data['password1'] = 'short'
        self.user_data['password2'] = 'short'
        form = CustomUserCreationForm(data=self.user_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'],
                         ['This password is too short. It must contain at least 8 characters.'])
