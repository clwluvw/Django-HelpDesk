# Generated by Django 2.2 on 2019-04-23 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='lastUpdate',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
