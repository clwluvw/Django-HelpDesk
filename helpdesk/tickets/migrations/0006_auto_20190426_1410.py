# Generated by Django 2.2 on 2019-04-26 09:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_auto_20190426_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='dateTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
