# Generated by Django 2.1.5 on 2019-03-22 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0015_auto_20190320_1303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trial',
            options={'ordering': ('time_start',), 'verbose_name': 'trial', 'verbose_name_plural': 'trials'},
        ),
    ]
