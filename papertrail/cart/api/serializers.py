from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from cart.models import Cart, CartItem
from books.models import Book, Author


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ('title',)


class BookSerializer(ModelSerializer):
    author = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'cover_image', 'price')


class ProductSerializer(ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'quantity', 'book')


class CartSerializer(ModelSerializer):
    products = ProductSerializer(many=True)
    total_price = serializers.FloatField()

    class Meta:
        model = Cart
        fields = ('id', 'total_price', 'products')


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'quantity')
