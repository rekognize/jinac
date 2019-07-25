# Generated by Django 2.1.5 on 2019-07-25 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0006_observer'),
        ('cases', '0041_remove_case_complainant'),
    ]

    operations = [
        migrations.AddField(
            model_name='trial',
            name='inst_observers',
            field=models.ManyToManyField(blank=True, to='institutions.Observer', verbose_name='institutional observers'),
        ),
    ]
