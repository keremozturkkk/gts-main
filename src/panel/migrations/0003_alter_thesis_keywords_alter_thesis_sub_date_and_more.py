# Generated by Django 5.0.1 on 2024-01-05 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_remove_thesis_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesis',
            name='keywords',
            field=models.ManyToManyField(blank=True, null=True, to='panel.keyword'),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='sub_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='subjects',
            field=models.ManyToManyField(blank=True, null=True, to='panel.subject'),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='write_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
