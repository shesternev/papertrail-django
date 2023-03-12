from celery import shared_task

from django.core.mail import send_mass_mail

from papertrail.settings import EMAIL_HOST_USER
from account.models import User
from .models import MailingList


@shared_task
def mailing_to_active_users():
    active_users = User.objects.filter(is_active=True)
    emails = [user.email for user in active_users]

    newsletters = MailingList.objects.filter(is_active=True)
    messages = tuple(
        (newsletter.subject, newsletter.massage, EMAIL_HOST_USER, emails) for newsletter in newsletters
    )

    send_mass_mail(messages)
