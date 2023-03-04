from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from books.models import (
    Category,
    Book,
    Author,
    Publisher,
    Series,
    Interpreter,
    Illustrator,
    Illustrations,
    Paper,
    Font,
    Binding,
    Language,
    Review
)
from books.utils import get_parent_categories_from_child_to_parent


class CategoryListSerializer(ModelSerializer):
    subcategories = SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'slug', 'subcategories')

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        serializer = self.__class__(subcategories, many=True)
        return serializer.data


class BookAuthorDetailSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ('title',)


class BookListSerializer(ModelSerializer):
    author = BookAuthorDetailSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'price', 'slug', 'cover_image', 'author')


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)


class BookCategorySerializer(ModelSerializer):
    parent_categories = SerializerMethodField()

    class Meta:
        model = Category
        fields = ('title', 'parent_categories')

    @staticmethod
    def get_parent_categories(obj):
        subcategories = get_parent_categories_from_child_to_parent(obj, CategorySerializer)
        return subcategories


class BookPublisherSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('id', 'title', 'slug')


class BookAuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'title', 'slug')


class BookSeriesSerializer(ModelSerializer):
    class Meta:
        model = Series
        fields = ('id', 'title', 'slug')


class BookInterpreterSerializer(ModelSerializer):
    class Meta:
        model = Interpreter
        fields = ('id', 'title', 'slug')


class BookIllustratorSerializer(ModelSerializer):
    class Meta:
        model = Illustrator
        fields = ('id', 'title', 'slug')


class BookIllustrationsSerializer(ModelSerializer):
    class Meta:
        model = Illustrations
        fields = ('title',)


class BookPaperSerializer(ModelSerializer):
    class Meta:
        model = Paper
        fields = ('title',)


class BookFontSerializer(ModelSerializer):
    class Meta:
        model = Font
        fields = ('title',)


class BookBindingSerializer(ModelSerializer):
    class Meta:
        model = Binding
        fields = ('title',)


class BookLanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = ('title',)


class BookReviewSerializer(ModelSerializer):
    user_first_name = serializers.CharField(source='user.first_name')
    user_last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Review
        fields = ('user', 'user_first_name', 'user_last_name', 'title', 'content', 'rating', 'created')


class BookDetailSerializer(ModelSerializer):
    category = BookCategorySerializer(many=False)
    publisher = BookPublisherSerializer(many=True)
    author = BookAuthorSerializer(many=True)
    series = BookSeriesSerializer(many=True)
    interpreter = BookInterpreterSerializer(many=True)
    illustrator = BookIllustratorSerializer(many=True)
    illustrations = BookIllustrationsSerializer(many=True)
    paper = BookPaperSerializer(many=True)
    font = BookFontSerializer(many=True)
    binding = BookBindingSerializer(many=True)
    language = BookLanguageSerializer(many=True)
    reviews = BookReviewSerializer(many=True)

    class Meta:
        model = Book
        fields = (
            'title', 'cover_image', 'price', 'slug', 'year_of_first_publication', 'year_of_publication', 'amount_pages',
            'weight', 'edition', 'literature_of_the_countries_of_the_world', 'format', 'isbn', 'category', 'publisher',
            'author', 'series', 'interpreter', 'illustrator', 'illustrations', 'paper', 'font', 'binding', 'language',
            'reviews'
        )


class PublisherDetailSerializer(ModelSerializer):
    books = BookListSerializer(many=True)

    class Meta:
        model = Publisher
        fields = ('id', 'title', 'image', 'description', 'slug', 'books')


class AuthorDetailSerializer(ModelSerializer):
    books = BookListSerializer(many=True)

    class Meta:
        model = Author
        fields = ('id', 'title', 'image', 'biography', 'slug', 'books')


class SeriesDetailSerializer(ModelSerializer):
    books = BookListSerializer(many=True)

    class Meta:
        model = Series
        fields = ('id', 'title', 'slug', 'books')


class InterpreterDetailSerializer(ModelSerializer):
    books = BookListSerializer(many=True)

    class Meta:
        model = Interpreter
        fields = ('id', 'title', 'slug', 'books')


class IllustratorDetailSerializer(ModelSerializer):
    books = BookListSerializer(many=True)

    class Meta:
        model = Illustrator
        fields = ('id', 'title', 'slug', 'books')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('book', 'user', 'title', 'content', 'rating')
