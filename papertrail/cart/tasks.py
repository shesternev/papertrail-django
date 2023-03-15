from datetime import datetime, timedelta

from celery import shared_task

from .models import Cart


@shared_task
def delete_old_carts():
    two_weeks_ago = datetime.now() - timedelta(days=14)
    old_carts = Cart.objects.filter(created_ad__lt=two_weeks_ago)
    old_carts.delete()
