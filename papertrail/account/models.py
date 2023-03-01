from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, phone_number, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, phone_number, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name='email address'
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='phone number'
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='first name'
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='last name'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='active'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='staff status'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='superuser status'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date joined'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True
