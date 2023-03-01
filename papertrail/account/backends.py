from django.contrib.auth.backends import BaseBackend
from .models import User


class EmailBackend(BaseBackend):
    def authenticate(self, request, **kwargs):

        email = kwargs.get('username')
        password = kwargs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class PhoneBackend(BaseBackend):
    def authenticate(self, request, **kwargs):

        phone_number = kwargs.get('username')
        password = kwargs.get('password')

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
