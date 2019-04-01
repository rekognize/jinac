# Generated by Django 2.1.5 on 2019-03-30 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0018_auto_20190329_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='summary',
            field=models.TextField(blank=True, null=True, verbose_name='case summary'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='summary',
            field=models.TextField(default='-', verbose_name='case summary'),
            preserve_default=False,
        ),
    ]