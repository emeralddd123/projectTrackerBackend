# Generated by Django 4.1.5 on 2023-02-06 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreApi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='slug',
            field=models.SlugField(blank=True, editable=False, unique=True),
        ),
    ]
