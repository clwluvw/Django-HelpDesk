# Generated by Django 2.2 on 2019-04-29 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='approved',
        ),
    ]
