# Generated by Django 2.1.5 on 2019-04-25 20:52

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0028_auto_20190418_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalistnote',
            name='note',
            field=martor.models.MartorField(verbose_name='note'),
        ),
        migrations.AlterField(
            model_name='person',
            name='bio',
            field=martor.models.MartorField(blank=True, null=True, verbose_name='biography'),
        ),
        migrations.AlterField(
            model_name='person',
            name='short_bio',
            field=martor.models.MartorField(blank=True, null=True, verbose_name='short bio'),
        ),
    ]
