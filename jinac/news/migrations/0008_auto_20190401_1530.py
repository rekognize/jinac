# Generated by Django 2.1.5 on 2019-04-01 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20190318_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='text',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='text'),
        ),
    ]
