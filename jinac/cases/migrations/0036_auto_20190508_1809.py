# Generated by Django 2.1.5 on 2019-05-08 18:09

from django.db import migrations, models
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0035_casenote_note_en'),
    ]

    operations = [
        migrations.AddField(
            model_name='casenotetype',
            name='type_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='type (EN)'),
        ),
        migrations.AlterField(
            model_name='casenote',
            name='note_en',
            field=martor.models.MartorField(blank=True, null=True, verbose_name='note (EN)'),
        ),
    ]