from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse

from account.models import User
from books.models import (
    Category,
    Book,
    Author,
    Publisher,
    Series,
    Interpreter,
    Illustrator
)
from books.api.serializers import (
    CategoryListSerializer,
    BookListSerializer,
    BookDetailSerializer,
    PublisherDetailSerializer,
    AuthorDetailSerializer,
    SeriesDetailSerializer,
    InterpreterDetailSerializer,
    IllustratorDetailSerializer
)


class CategoryListAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        category_1 = Category.objects.create(
            title='Category 1'
        )
        subcategory_1 = Category.objects.create(
            title='Subcategory 1',
            parent=category_1
        )

        category_2 = Category.objects.create(
            title='Category 2',
        )

        self.category_1 = category_1
        self.category_2 = category_2
        self.subcategory_1 = subcategory_1

    def test_get(self):
        url = reverse('category-list')
        response = self.client.get(url)
        response_data = response.data
        excepted_data = CategoryListSerializer([self.category_1, self.category_2], many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('results'), excepted_data)

    def test_count(self):
        url = reverse('category-list')
        response = self.client.get(url)
        response_data = response.data

        self.assertEqual(response_data.get('count'), 2)

    def test_category_include_children(self):
        url = reverse('category-list')
        response = self.client.get(url)

        category_1_data = response.data['results'][0]
        category_1_subcategories = category_1_data['subcategories']
        excepted_data = CategoryListSerializer([self.subcategory_1], many=True).data

        self.assertEqual(category_1_subcategories, excepted_data)


class BookListAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        book_1 = Book.objects.create(
            title='Book 1',
            cover_image='http://testserver/media/path%20to%20image',
            price=150.00,
            category=Category.objects.create(
                title='Category 1'
            )
        )
        book_2 = Book.objects.create(
            title='Book 2',
            cover_image='http://testserver/media/path%20to%20image',
            price=100.00,
            category=Category.objects.create(
                title='Category 2'
            )
        )

        self.book_1 = book_1
        self.book_2 = book_2

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        response_data = response.data
        excepted_data = BookListSerializer([self.book_1, self.book_2], many=True).data

        for item in excepted_data:
            item['cover_image'] = 'http://testserver/media/http%3A/testserver/media/path%2520to%2520image'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('results'), excepted_data)

    def test_count(self):
        url = reverse('book-list')
        response = self.client.get(url)
        response_data = response.data

        self.assertEqual(response_data.get('count'), 2)

    def test_search(self):
        author = Author.objects.create(title='Author')

        self.book_1.author.add(author)
        self.book_1.save()
        self.book_2.title = 'Book Author'
        self.book_2.save()

        url = reverse('book-list')
        response_data = self.client.get(url, data={'search': 'Author'}).data
        excepted_data = BookListSerializer([self.book_2, self.book_1], many=True).data

        for item in excepted_data:
            item['cover_image'] = 'http://testserver/media/http%3A/testserver/media/path%2520to%2520image'

        self.assertEqual(response_data.get('results'), excepted_data)

    def test_ordering(self):
        url = reverse('book-list')
        response_data = self.client.get(url, data={'ordering': 'price'}).data
        excepted_data = BookListSerializer([self.book_2, self.book_1], many=True).data

        for item in excepted_data:
            item['cover_image'] = 'http://testserver/media/http%3A/testserver/media/path%2520to%2520image'

        self.assertEqual(response_data.get('results'), excepted_data)

        response_data = self.client.get(url, data={'ordering': '-price'}).data
        excepted_data = BookListSerializer([self.book_1, self.book_2], many=True).data

        for item in excepted_data:
            item['cover_image'] = 'http://testserver/media/http%3A/testserver/media/path%2520to%2520image'

        self.assertEqual(response_data.get('results'), excepted_data)

    def test_filter(self):
        publisher_1 = Publisher.objects.create(title='Publisher 1')
        publisher_2 = Publisher.objects.create(title='Publisher 2')

        author = Author.objects.create(title='Author 1')

        self.book_1.publisher.add(publisher_1, publisher_2)
        self.book_2.publisher.add(publisher_1)
        self.book_2.author.add(author)

        url = reverse('book-list')
        response_data = self.client.get(url, data={
            'publisher': (publisher_1.id, publisher_2.id),
            'author': (author.id,)
        }).data
        excepted_data = BookListSerializer([self.book_2], many=True).data

        for item in excepted_data:
            item['cover_image'] = 'http://testserver/media/http%3A/testserver/media/path%2520to%2520image'

        self.assertEqual(response_data.get('results'), excepted_data)

    def test_min_and_max_price(self):
        url = reverse('book-list')
        response_data = self.client.get(url, data={
            'min_price': 149,
            'max_price': 610
        }).data
        excepted_data = BookListSerializer([self.book_1], many=True).data

        for item in excepted_data:
            item['cover_image'] = 'http://testserver/media/http%3A/testserver/media/path%2520to%2520image'

        self.assertEqual(response_data.get('results'), excepted_data)


class BookDetailRetrieveAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        book_1 = Book.objects.create(
            title='Book 1',
            cover_image='http://testserver/media/path%20to%20image',
            price=150.00,
            category=Category.objects.create(title='Category 1')
        )

        self.book_1 = book_1

    def test_get(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        response = self.client.get(url)
        response_data = response.data
        excepted_data = BookDetailSerializer(self.book_1, many=False).data

        excepted_data['cover_image'] = 'http://testserver/media/http%3A/testserver/media/path%2520to%2520image'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, excepted_data)

    def test_count_fields(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        response = self.client.get(url)
        response_data = response.data
        excepted_data = BookDetailSerializer(self.book_1, many=False).data

        self.assertEqual(len(response_data), len(excepted_data))
        self.assertEqual(len(response_data), 24)


class PublisherDetailRetrieveAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        publisher_1 = Publisher.objects.create(title='Publisher 1')

        self.publisher_1 = publisher_1

    def test_get(self):
        url = reverse('publisher-detail', args=(self.publisher_1.id,))
        response = self.client.get(url)
        response_data = response.data
        excepted_data = PublisherDetailSerializer(self.publisher_1, many=False).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, excepted_data)

    def test_count_fields(self):
        url = reverse('publisher-detail', args=(self.publisher_1.id,))
        response = self.client.get(url)
        response_data = response.data
        excepted_data = PublisherDetailSerializer(self.publisher_1, many=False).data

        self.assertEqual(len(response_data), len(excepted_data))
        self.assertEqual(len(response_data), 6)


class AuthorDetailRetrieveAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        author_1 = Author.objects.create(title='Author 1')

        self.author_1 = author_1

    def test_get(self):
        url = reverse('author-detail', args=(self.author_1.id,))
        response = self.client.get(url)
        response_data = response.data
        excepted_data = AuthorDetailSerializer(self.author_1, many=False).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, excepted_data)

    def test_count_fields(self):
        url = reverse('author-detail', args=(self.author_1.id,))
        response = self.client.get(url)
        response_data = response.data
        excepted_data = AuthorDetailSerializer(self.author_1, many=False).data

        self.assertEqual(len(response_data), len(excepted_data))
        self.assertEqual(len(response_data), 6)


class SeriesDetailRetrieveAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        series_1 = Series.objects.create(title='Series 1')

        self.series_1 = series_1

    def test_get(self):
        url = reverse('series-detail', args=(self.series_1.id,))
        response = self.client.get(url)
        response_data = response.data
        excepted_data = SeriesDetailSerializer(self.series_1, many=False).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, excepted_data)

    def test_count_fields(self):
        url = reverse('series-detail', args=(self.series_1.id,))
        response = self.client.get(url)
        response_data = response.data
        excepted_data = SeriesDetailSerializer(self.series_1, many=False).data

        self.assertEqual(len(response_data), len(excepted_data))
        self.assertEqual(len(response_data), 4)


class InterpreterDetailRetrieveAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        interpreter_1 = Interpreter.objects.create(title='Interpreter 1')

        self.interpreter_1 = interpreter_1

    def test_get(self):
        url = reverse('interpreter-detail', args=(self.interpreter_1.id,))
        response = self.client.get(url)
        response_data = response.data
        excepted_data = InterpreterDetailSerializer(self.interpreter_1, many=False).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, excepted_data)

    def test_count_fields(self):
        url = reverse('interpreter-detail', args=(self.interpreter_1.id,))
        response = self.client.get(url)
        response_data = response.data
        excepted_data = InterpreterDetailSerializer(self.interpreter_1, many=False).data

        self.assertEqual(len(response_data), len(excepted_data))
        self.assertEqual(len(response_data), 4)


class IllustratorDetailRetrieveAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        illustrator_1 = Illustrator.objects.create(title='Illustrator 1')

        self.illustrator_1 = illustrator_1

    def test_get(self):
        url = reverse('illustrator-detail', args=(self.illustrator_1.id,))
        response = self.client.get(url)
        response_data = response.data
        excepted_data = IllustratorDetailSerializer(self.illustrator_1, many=False).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, excepted_data)

    def test_count_fields(self):
        url = reverse('illustrator-detail', args=(self.illustrator_1.id,))
        response = self.client.get(url)
        response_data = response.data
        excepted_data = IllustratorDetailSerializer(self.illustrator_1, many=False).data

        self.assertEqual(len(response_data), len(excepted_data))
        self.assertEqual(len(response_data), 4)


class ReviewCreateAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        user_1 = User.objects.create_user(
            phone_number='000000000',
            email='mail@mail.com'
        )
        book_1 = Book.objects.create(
            title='Book 1',
            cover_image='http://testserver/media/path%20to%20image',
            price=150.00,
            category=Category.objects.create(title='Category 1')
        )

        review_data = {
            "book": book_1.id,
            "user": user_1.id,
            "title": "Title 1",
            "content": "Content 1",
            "rating": 5
        }

        self.user_1 = user_1
        self.book_1 = book_1
        self.review_data = review_data

    def test_post(self):
        url = reverse('review-create')
        client = APIClient()
        client.force_authenticate(user=self.user_1)
        response = client.post(url, data=self.review_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.review_data)
        self.assertEqual(len(response.data), len(self.review_data))
        self.assertEqual(len(response.data), 5)
