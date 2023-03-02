from django.test import TestCase
from django.urls import reverse

from account.models import User
from books.models import Category
from books.admin import CategoryAdmin


class CategoryAdminTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            phone_number='0000000000',
            email='admin@test.com',
            password='admin123'
        )

        self.category = Category.objects.create(
            title='Test Category',
            slug='test-category'
        )

        self.client.login(username='0000000000', password='admin123')

    def test_category_admin_list_display(self):
        expected = ('title', 'parent')
        result = CategoryAdmin.list_display
        self.assertSequenceEqual(result, expected)

    def test_category_admin_prepopulated_fields(self):
        expected = {'slug': ('title',)}
        result = CategoryAdmin.prepopulated_fields
        self.assertDictEqual(result, expected)

    def test_category_admin_create(self):
        url = reverse('admin:books_category_add')
        data = {
            'title': 'New Category',
            'parent': self.category.pk,
            'slug': 'new-category'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
