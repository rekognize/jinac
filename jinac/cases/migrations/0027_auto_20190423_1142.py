# Generated by Django 2.1.5 on 2019-04-23 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0026_auto_20190423_1124'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casenote',
            options={'ordering': ('case', 'type'), 'verbose_name': 'journalist note', 'verbose_name_plural': 'journalist notes'},
        ),
    ]
