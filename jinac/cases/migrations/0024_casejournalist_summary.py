# Generated by Django 2.1.5 on 2019-04-23 07:13

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0023_auto_20190418_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='casejournalist',
            name='summary',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='note'),
        ),
    ]