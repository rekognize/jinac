# Generated by Django 2.1.5 on 2019-03-08 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0005_auto_20190307_0905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indictment',
            name='category',
        ),
    ]
