# Generated by Django 2.1.5 on 2019-05-08 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0033_auto_20190508_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casenote',
            name='lang',
        ),
    ]
