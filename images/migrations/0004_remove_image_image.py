# Generated by Django 3.1.6 on 2021-05-17 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_auto_20210517_1736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image',
        ),
    ]
