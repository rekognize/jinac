# Generated by Django 2.1.5 on 2019-05-08 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0037_auto_20190508_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
