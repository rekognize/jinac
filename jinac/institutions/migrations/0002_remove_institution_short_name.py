# Generated by Django 2.1.5 on 2019-02-07 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='short_name',
        ),
    ]
