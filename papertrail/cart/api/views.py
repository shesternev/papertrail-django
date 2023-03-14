from rest_framework.viewsets import ModelViewSet

from django.db.models import Prefetch, Sum, ExpressionWrapper, F, FloatField

from books.models import Book, Author
from cart.models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all().prefetch_related(
        Prefetch('products', queryset=CartItem.objects.all().prefetch_related(
            Prefetch('book', queryset=Book.objects.all().prefetch_related(
                Prefetch('author', queryset=Author.objects.all().only('title'))
            ).only('id', 'title', 'author', 'cover_image', 'price'))
        ))
    ).annotate(total_price=ExpressionWrapper(
        Sum(F('products__book__price') * F('products__quantity')), output_field=FloatField())
    )
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all().only('id', 'quantity')
    serializer_class = CartItemSerializer
