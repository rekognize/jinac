# Generated by Django 2.1.5 on 2019-03-16 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0013_auto_20190316_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='punishment_amount_max',
        ),
        migrations.RemoveField(
            model_name='article',
            name='punishment_amount_min',
        ),
    ]
