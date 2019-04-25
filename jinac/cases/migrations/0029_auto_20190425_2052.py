# Generated by Django 2.1.5 on 2019-04-25 20:52

from django.db import migrations, models
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0028_auto_20190423_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='summary',
            field=martor.models.MartorField(blank=True, null=True, verbose_name='case summary'),
        ),
        migrations.AlterField(
            model_name='casenote',
            name='note',
            field=martor.models.MartorField(verbose_name='note'),
        ),
        migrations.AlterField(
            model_name='casestatus',
            name='details',
            field=models.TextField(blank=True, null=True, verbose_name='details'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='summary',
            field=martor.models.MartorField(verbose_name='case summary'),
        ),
        migrations.AlterField(
            model_name='trialnote',
            name='note',
            field=martor.models.MartorField(blank=True, null=True, verbose_name='note'),
        ),
    ]
