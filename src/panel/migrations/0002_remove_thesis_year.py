# Generated by Django 5.0.1 on 2024-01-03 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thesis',
            name='year',
        ),
    ]
