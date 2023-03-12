from django.db import models


class MailingList(models.Model):
    subject = models.CharField(
        max_length=255,
        verbose_name='Message subject'
    )
    massage = models.CharField(
        max_length=550,
        verbose_name='Message content'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Active mailing'
    )

    class Meta:
        verbose_name = 'mailing list'
        verbose_name_plural = 'Mailing list'

    def __str__(self):
        return self.subject
