# Generated by Django 2.1.5 on 2019-09-11 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0048_auto_20190823_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'TCK'), (2, 'TMK'), (4, 'MİT'), (5, 'TGYK')]),
        ),
    ]
