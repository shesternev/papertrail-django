# Generated by Django 3.2.18 on 2023-03-15 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20230315_1311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='created_ad',
            new_name='created_at',
        ),
    ]
