# Generated by Django 2.1.5 on 2019-03-10 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0009_auto_20190310_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='journalist_defendant_count',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='journalist defendant count'),
        ),
    ]
