# Generated by Django 2.1.5 on 2019-09-11 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0018_auto_20190708_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='value',
            field=models.CharField(max_length=250, verbose_name='value'),
        ),
    ]
