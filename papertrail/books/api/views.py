from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters

from django.db.models import Prefetch, Avg

from .serializers import (
    CategoryListSerializer,
    BookListSerializer,
    BookDetailSerializer,
    PublisherDetailSerializer,
    AuthorDetailSerializer,
    SeriesDetailSerializer,
    InterpreterDetailSerializer,
    IllustratorDetailSerializer,
    ReviewCreateSerializer,
)
from books.models import (
    Category,
    Book,
    Author,
    Review,
    Publisher,
    Series,
    Interpreter,
    Illustrator,
)
from books.filters import BookListFilter


class CategoryListAPIView(ListAPIView):
    """
    This class-based view returns a list of categories,
    where each category may have subcategories up to six levels deep.
    """
    queryset = Category.objects.filter(parent=None).prefetch_related(
        Prefetch('subcategories', queryset=Category.objects.prefetch_related(
            Prefetch('subcategories', queryset=Category.objects.prefetch_related(
                Prefetch('subcategories', queryset=Category.objects.prefetch_related(
                    Prefetch('subcategories', queryset=Category.objects.prefetch_related(
                        Prefetch('subcategories', queryset=Category.objects.all())
                    ))
                ))
            ))
        ))
    )
    serializer_class = CategoryListSerializer


class BookListAPIView(ListAPIView):
    queryset = Book.objects.all().prefetch_related(
        Prefetch('author', queryset=Author.objects.all().only('id', 'title')),
    ).only('id', 'title', 'price', 'slug', 'cover_image')
    serializer_class = BookListSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = BookListFilter
    search_fields = (
        'title',
        'author__title',
        'series__title',
        'publisher__title',
        'interpreter__title',
        'illustrator__title'
    )
    ordering_fields = ('price',)


class BookDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Book.objects.select_related('category__parent').prefetch_related(
        Prefetch('publisher', queryset=Publisher.objects.all().only('title', 'slug')),
        Prefetch('author', queryset=Author.objects.all().only('title', 'slug')),
        Prefetch('reviews', queryset=Review.objects.select_related('user', 'book').only(
            'id', 'title', 'content', 'rating', 'created',
            'book__id', 'user__first_name', 'user__last_name').all())
    ).annotate(average_rating=Avg('reviews__rating')).only(
        'title', 'cover_image', 'price', 'slug', 'year_of_first_publication', 'year_of_publication', 'amount_pages',
        'weight', 'edition', 'literature_of_the_countries_of_the_world', 'format', 'isbn', 'category', 'publisher',
        'author', 'series', 'interpreter', 'illustrator', 'illustrations', 'paper', 'font', 'binding', 'language',
    ).filter()
    serializer_class = BookDetailSerializer


class PublisherDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Publisher.objects.all().prefetch_related(
        Prefetch('books', queryset=Book.objects.all().prefetch_related(
            Prefetch('author', queryset=Author.objects.all().only('title'))
        ).only('id', 'title', 'price', 'slug', 'cover_image'))
    )
    serializer_class = PublisherDetailSerializer


class AuthorDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Author.objects.all().prefetch_related(
        Prefetch('books', queryset=Book.objects.all().prefetch_related(
            Prefetch('author', queryset=Author.objects.all().only('title'))
        ).only('id', 'title', 'price', 'slug', 'cover_image'))
    )
    serializer_class = AuthorDetailSerializer


class SeriesDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Series.objects.all().prefetch_related(
        Prefetch('books', queryset=Book.objects.all().prefetch_related(
            Prefetch('author', queryset=Author.objects.all().only('title'))
        ).only('id', 'title', 'price', 'slug', 'cover_image'))
    )
    serializer_class = SeriesDetailSerializer


class InterpreterDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Interpreter.objects.prefetch_related(
        Prefetch('books', queryset=Book.objects.all().prefetch_related(
            Prefetch('author', queryset=Author.objects.all().only('title'))
        ).only('id', 'title', 'price', 'slug', 'cover_image'))
    )
    serializer_class = InterpreterDetailSerializer


class IllustratorDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Illustrator.objects.prefetch_related(
        Prefetch('books', queryset=Book.objects.all().prefetch_related(
            Prefetch('author', queryset=Author.objects.all().only('title'))
        ).only('id', 'title', 'price', 'slug', 'cover_image'))
    )
    serializer_class = IllustratorDetailSerializer


class ReviewCreateAPIView(CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]
