# Generated by Django 2.1.5 on 2019-03-27 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20190327_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='title'),
        ),
    ]
