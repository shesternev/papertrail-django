from unittest.mock import Mock

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from account.admin import UserAdmin


class UserAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user_admin = UserAdmin(get_user_model(), self.site)
        self.request = Mock()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='password123',
            phone_number='+1234567890',
            first_name='John',
            last_name='Doe',
            is_staff=True,
            is_superuser=False
        )

    def test_ordering(self):
        self.assertEqual(self.user_admin.ordering, ('id',))

    def test_list_filter(self):
        self.assertEqual(self.user_admin.list_filter, ('is_active', 'is_staff'))

    def test_readonly_fields(self):
        self.assertEqual(self.user_admin.readonly_fields, ('date_joined', 'last_login'))

    def test_filter_horizontal(self):
        self.assertEqual(self.user_admin.filter_horizontal, ('groups', 'user_permissions'))

    def test_search_fields(self):
        self.assertEqual(self.user_admin.search_fields, ('email', 'phone_number', 'first_name', 'last_name'))

    def test_list_display(self):
        self.assertEqual(self.user_admin.list_display, ('id', 'email', 'phone_number', 'is_staff', 'is_active'))

    def test_add_fieldsets(self):
        add_fieldsets = list(self.user_admin.add_fieldsets)
        self.assertEqual(len(add_fieldsets), 1)

        add_fieldset = add_fieldsets[0]
        self.assertEqual(add_fieldset[0], None)
        self.assertEqual(add_fieldset[1]['classes'], ('wide',))
        self.assertEqual(set(add_fieldset[1]['fields']),
                         {'email', 'phone_number', 'first_name', 'last_name', 'password1', 'password2'})

    def test_fieldsets(self):
        fieldsets = list(self.user_admin.fieldsets)
        self.assertEqual(len(fieldsets), 4)

        first_fieldset = fieldsets[0]
        self.assertEqual(first_fieldset[0], None)
        self.assertEqual(set(first_fieldset[1]['fields']), {'email', 'phone_number', 'password'})

        second_fieldset = fieldsets[1]
        self.assertEqual(second_fieldset[0], _('Personal info'))
        self.assertEqual(set(second_fieldset[1]['fields']), {'first_name', 'last_name'})

        third_fieldset = fieldsets[2]
        self.assertEqual(third_fieldset[0], _('Permissions'))
        self.assertEqual(set(third_fieldset[1]['fields']),
                         {'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'})

        fourth_fieldset = fieldsets[3]
        self.assertEqual(fourth_fieldset[0], _('Dates'))
        self.assertEqual(set(fourth_fieldset[1]['fields']), {'last_login', 'date_joined'})
