# Generated by Django 3.0.6 on 2020-06-07 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searcher', '0005_imageproperty_format_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='img_format',
            field=models.CharField(default='png', max_length=10),
        ),
    ]