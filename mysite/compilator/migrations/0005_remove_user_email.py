# Generated by Django 4.1.7 on 2023-05-25 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compilator', '0004_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
    ]