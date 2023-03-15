import uuid

from django.db import models

from books.models import Book


class Cart(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateField(
        auto_now_add=True,
        auto_created=True,
        editable=False
    )


class CartItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        related_name='products'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(
        default=1
    )
