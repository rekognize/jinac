# Generated by Django 2.1.5 on 2019-04-27 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_feed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feed',
            options={'ordering': ('-time',), 'verbose_name': 'Feed', 'verbose_name_plural': 'Feed'},
        ),
    ]