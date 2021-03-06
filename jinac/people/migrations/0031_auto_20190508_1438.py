# Generated by Django 2.1.5 on 2019-05-08 14:38

from django.db import migrations, models
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0030_auto_20190425_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='bio_en',
            field=martor.models.MartorField(blank=True, null=True, verbose_name='biography (EN)'),
        ),
        migrations.AddField(
            model_name='person',
            name='short_bio_en',
            field=models.TextField(blank=True, null=True, verbose_name='short bio (EN)'),
        ),
    ]
