from django.test import TestCase
from books.models import Category, Author, Publisher


class CategoryModelTest(TestCase):
    def test_category_string_representation(self):
        category = Category(title='Fiction')
        self.assertEqual(str(category), category.title)

    def test_category_parent_can_be_null(self):
        category = Category(title='Fiction', parent=None)
        self.assertEqual(category.parent, None)

    def test_category_children_can_be_accessed(self):
        parent_category = Category(title='Fiction')
        child_category = Category(title='Mystery', parent=parent_category)
        parent_category.save()
        child_category.save()
        self.assertEqual(child_category.parent, parent_category)
        self.assertIn(child_category, parent_category.children.all())


class AuthorModelTest(TestCase):
    def test_author_string_representation(self):
        author = Author(title='Harper Lee')
        self.assertEqual(str(author), author.title)

    def test_author_slug_is_filled_in_automatically(self):
        author = Author(title='Harper Lee')
        author.save()
        self.assertEqual(author.slug, 'harper-lee')


class PublisherModelTest(TestCase):
    def test_publisher_string_representation(self):
        publisher = Publisher(title='Penguin Random House')
        self.assertEqual(str(publisher), publisher.title)

    def test_publisher_slug_is_filled_in_automatically(self):
        publisher = Publisher(title='Penguin Random House')
        publisher.save()
        self.assertEqual(publisher.slug, 'penguin-random-house')
