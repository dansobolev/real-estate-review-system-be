# Generated by Django 3.1.6 on 2021-02-25 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0005_city_country_region_subregion'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city', to='property.city'),
        ),
    ]
